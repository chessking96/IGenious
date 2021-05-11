#pragma once

#include <iostream>
#include <algorithm>
#include "igen_lib.h"
#include "igen_dd_lib.h"

using namespace std;

/* Parameter */
#define BUCKET_SIZE  24
#define BUCKET_SHIFT (3*BUCKET_SIZE/4)

typedef union {
    unsigned long u;
    double d;
} bitDouble;

static unsigned get_exp(double a) {
    bitDouble _a;
    _a.d = a;
    _a.u = (_a.u & 0x7FFFFFFFFFFFFFFFu);
    return _a.u >> 52u;
}

static bool is_even (double a) {
    bitDouble _a;
    _a.d = a;
    _a.u = (_a.u & 0x01u);
    return _a.u;
}

static unsigned get_lsb (double a) {
    bitDouble _a;
    _a.d = a;
    _a.u = (_a.u & 0x01u);
    return _a.u;
}

class acc_f64_dyn_t {
public:
    double even_bucket[BUCKET_SIZE];
    double odd_bucket[BUCKET_SIZE];
    int    min_exp;

    acc_f64_dyn_t() : even_bucket(), odd_bucket(), min_exp(0) { /* This initializes to zero the arrays */ }

    /// Get the bucket index based on the exponent
    int get_bucket_index(double d) {
        int exp = (int) get_exp(d);
        int index = exp - min_exp;

        if (index < 0) {
            /* Underflow to the lowest exponent */
            index = 0;
        }

        if (index >= BUCKET_SIZE) {
            /* Overflow, the exponent is larger than the max supported. Shift bucket dynamic window. */
            int new_min_exp = exp - BUCKET_SHIFT;

            /* Reduce elements from min_exp to new_min_exp, and place it in the lowest bucket */
            int new_min_index = new_min_exp - min_exp + 1;
            double sum1 = 0.0, sum2 = 0.0;
            for (int i = 0; i < new_min_index && i < BUCKET_SIZE; i++) {
                sum1 += even_bucket[i];
                sum2 += odd_bucket[i];
                even_bucket[i] = 0.0;
                odd_bucket[i]  = 0.0;
            }
            even_bucket[0] = sum1;
            odd_bucket[0]  = sum2;

            /* Now shift the remaining elements to the lower buckets */
            int j = 1;
            for (int i = new_min_index; i < BUCKET_SIZE; i++) {
                even_bucket[j] = even_bucket[i];
                odd_bucket [j] = odd_bucket[i];
                even_bucket[i] = 0.0;
                odd_bucket [i] = 0.0;
                j++;
            }

            min_exp = new_min_exp;
            index = BUCKET_SHIFT;
        }

        return index;
    }

    void insert(double d) {
        static bool warn_underflow = true;
        unsigned i = get_bucket_index(d);
        double   t = d;

        if (i == 0) {
            /* This is the underflow bucket. Thus, handled separately */
            t += even_bucket[0] + odd_bucket[0];
            i = get_bucket_index(t);
            even_bucket[0] = 0.0;
            odd_bucket [0] = 0.0;

            if (warn_underflow) {
                std::cout << "underflow in precised exp sort" << std::endl;
                warn_underflow = false;
            }
        }

        double* bucket = is_even(t) ? even_bucket : odd_bucket;
        while (bucket[i] != 0.0 && i < BUCKET_SIZE) {
            t += bucket[i];
            bucket[i] = 0.0;
            i++;
            bucket = is_even(t) ? even_bucket : odd_bucket;
        }

        if (i >= BUCKET_SIZE) {
            /* Overflow occurs. Readjust bucket */
            i = get_bucket_index(t);
        }

        bucket[i] = t;
    }

    double reduce() {
        double sum1 = 0.0;
        double sum2 = 0.0;
        for (int i = 0; i < BUCKET_SIZE; i++) {
            sum1 = sum1 + even_bucket[i];
            sum2 = sum2 + odd_bucket[i];
        }
        return sum1 + sum2;
    }

    void clear () {
        std::fill(even_bucket, even_bucket+BUCKET_SIZE, 0);
        std::fill(odd_bucket, odd_bucket+BUCKET_SIZE, 0);
    }
};

class acc_f64_big_t {
public:
    double even_bucket[2048];
    double odd_bucket[2048];

    /* stats */
    int min_index = 0;
    int max_index = 0;

    acc_f64_big_t() : even_bucket(), odd_bucket() { /* This initializes to zero the arrays */ }

    /// Get the bucket index based on the exponent
    int get_bucket_index(double d) {
        return (int) get_exp(d);
    }

    void insert(double d) {
        unsigned i = get_bucket_index(d);
        double   t = d;

        double* bucket = is_even(t) ? even_bucket : odd_bucket;
        while (bucket[i] != 0.0) {
            t += bucket[i];
            bucket[i] = 0.0;
            i = get_bucket_index(t);
            bucket = is_even(t) ? even_bucket : odd_bucket;
        }

        bucket[i] = t;
    }

    double reduce() {
        double sum = 0.0;
        for (int i = 0; i < 2048; i++) {
            sum = sum + even_bucket[i] + odd_bucket[i];
        }
        return sum;
    }

    void clear () {
        std::fill(even_bucket, even_bucket+2048, 0);
        std::fill(odd_bucket, odd_bucket+2048, 0);
    }
};

class acc_f64_big2_t {
public:
    double bucket[4096];

    /* stats */
    int min_index = 0;
    int max_index = 0;

    acc_f64_big2_t() : bucket() { /* This initializes to zero the arrays */ }

    /// Get the bucket index based on the exponent
    unsigned get_bucket_index(double d) {
        unsigned exp = get_exp(d);
        unsigned lsb = get_lsb(d);
        return (exp << 1u) + lsb;
    }

    void insert(double d) {
        unsigned i = get_bucket_index(d);
        double   t = d;

        while (bucket[i] != 0.0) {
            t += bucket[i];
            bucket[i] = 0.0;
            i = get_bucket_index(t);
        }
        bucket[i] = t;
    }

    double reduce() {
        double sum = 0.0;
        for (int i = 0; i < 4096; i++) {
            sum = sum + bucket[i];
        }
        return sum;
    }

    void clear () {
        std::fill(bucket, bucket+4096, 0);
    }
};

class acc_f64i_dyn_t {
    /* We separate positive and negative (useful when reducing size of buffer)*/
    acc_f64_dyn_t up_pos;
    acc_f64_dyn_t up_neg;
    acc_f64_dyn_t lo_pos;
    acc_f64_dyn_t lo_neg;

public:
    acc_f64i_dyn_t () = default;

    void isum_init_f64(f64_I a) {
        /* Here we clean the buffers and init first value */
        up_pos.clear();
        up_neg.clear();
        lo_pos.clear();
        lo_neg.clear();

        isum_accumulate_f64(a);
    }

    void isum_accumulate_f64(f64_I a) {
        u_f64i* _a = (u_f64i*) &a;

        if (_a->up > 0.0) { up_pos.insert(_a->up); }
                     else { up_neg.insert(_a->up); }

        if (_a->lo > 0.0) { lo_pos.insert(_a->lo); }
                     else { lo_neg.insert(_a->lo); }
    }

    f64_I isum_reduce_f64() {
        u_f64i r;
        r.up = up_pos.reduce() + up_neg.reduce();
        r.lo = lo_pos.reduce() + lo_neg.reduce();
        return r.v;
    }
};

class acc_f64i_big_t {
    /* We separate positive and negative (useful when reducing size of buffer)*/
    acc_f64_big_t up;
    acc_f64_big_t lo;

public:
    acc_f64i_big_t () = default;

    void isum_init_f64(f64_I a) {
        /* Here we clean the buffers and init first value */
        up.clear();
        lo.clear();

        isum_accumulate_f64(a);
    }

    void isum_accumulate_f64(f64_I a) {
        u_f64i* _a = (u_f64i*) &a;

        up.insert(_a->up);
        lo.insert(_a->lo);
    }

    f64_I isum_reduce_f64() {
        u_f64i r;
        r.up = up.reduce();
        r.lo = lo.reduce();
        return r.v;
    }
};

/* Accumulator using double-double */
class acc_f64i_dd_t {
    /* We separate positive and negative (useful when reducing size of buffer)*/
    dd_I acc;

public:
    acc_f64i_dd_t () = default;

    void isum_init_f64(f64_I a) {
        u_f64i* _a = (u_f64i*) &a;
        acc = _ia_set_dd(_a->lo, -0.0, _a->up, 0.0);
    }

    void isum_accumulate_f64(f64_I a) {
        acc = _ia_add_dd_f64i(acc, a);

    }

    f64_I isum_reduce_f64() {
        u_ddi* _acc = (u_ddi*) &acc;
        u_f64i r;
        r.up = _acc->uh;
        r.lo = _acc->lh;
        return r.v;
    }
};

/* Use this as accumulator */
//typedef acc_f64i_dyn_t acc_f64i_t;
//typedef acc_f64i_big_t acc_f64i_t;
typedef acc_f64i_dd_t  acc_f64i_t;