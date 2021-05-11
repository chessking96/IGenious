#include "igen_lib.h"
#include "atlas_prefetch.h"
#include "igen_reduction.h"

extern "C" void ATL_dJIK56x56x56TN56x56x0_a1_b1_redu(const int M, const int N, const int K,
                                          f64_I alpha, const f64_I *__restrict A,
                                          const int lda, const f64_I *__restrict B,
                                          const int ldb, f64_I beta,
                                          f64_I *__restrict C, const int ldc);

/* With reduction improvement */
void ATL_dJIK56x56x56TN56x56x0_a1_b1_redu(const int M, const int N, const int K,
                                     f64_I alpha, const f64_I *__restrict A,
                                     const int lda, const f64_I *__restrict B,
                                     const int ldb, f64_I beta,
                                     f64_I *__restrict C, const int ldc)

{
  const f64_I *stM = A + 3136;
  const f64_I *stN = B + 3136;
  const f64_I *pfA = stM;
  const int incPFA0 = (((int)(stM - A)) * 4 * 1) / (56 * 56);
  const int incPFA = (1 > incPFA0) ? 1 : incPFA0;

  const int incAm = (3 * 56);
  const int incAn = -(56 * 56);

  const int incBm = -56;
  const int incBn = 56;

  const int incCn = (ldc)-56;
  f64_I *pC0 = C;
  const f64_I *pA0 = A;
  const f64_I *pB0 = B;
  int k;
  f64_I rA0;
  f64_I rA1;
  f64_I rA2;
  f64_I rA3;
  f64_I rB0;
  do {
    do {
      ATL_pfl1R(pfA);
      pfA += incPFA;
      acc_f64i_t _acc0;
      _acc0.isum_init_f64(pC0[0]);
      acc_f64i_t _acc1;
      _acc1.isum_init_f64(pC0[1]);
      acc_f64i_t _acc2;
      _acc2.isum_init_f64(pC0[2]);
      acc_f64i_t _acc3;
      _acc3.isum_init_f64(pC0[3]);
      for (k = 56; k; k -= 1) {
        rA0 = *pA0;
        rB0 = *pB0;
        f64_I _t1 = _ia_mul_f64(rA0, rB0);
        _acc0.isum_accumulate_f64(_t1);
        rA1 = pA0[1 * 56];
        f64_I _t2 = _ia_mul_f64(rA1, rB0);
        _acc1.isum_accumulate_f64(_t2);
        rA2 = pA0[2 * 56];
        f64_I _t3 = _ia_mul_f64(rA2, rB0);
        _acc2.isum_accumulate_f64(_t3);
        rA3 = pA0[3 * 56];
        f64_I _t4 = _ia_mul_f64(rA3, rB0);
        _acc3.isum_accumulate_f64(_t4);
        pA0 += 1;
        pB0 += 1;
      }
      pC0[0] = _acc0.isum_reduce_f64();
      pC0[1] = _acc1.isum_reduce_f64();
      pC0[2] = _acc2.isum_reduce_f64();
      pC0[3] = _acc3.isum_reduce_f64();
      pC0 += 4;
      pA0 += incAm;
      pB0 += incBm;
    } while (pA0 != stM);
    pC0 += incCn;
    pA0 += incAn;
    pB0 += incBn;
  } while (pB0 != stN);
}
