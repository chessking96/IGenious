#include "igen_lib.h"
void ATL_dJIK56x56x56TN56x56x0_a1_b1(const int M, const int N, const int K,
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
  f64_I rC0_0;
  f64_I rC1_0;
  f64_I rC2_0;
  f64_I rC3_0;
  do {
    do {
      __asm__ __volatile__("prefetchnta %0" : : "m"(*((char *)(pfA))));
      pfA += incPFA;
      rC0_0 = *pC0;
      rC1_0 = pC0[1];
      rC2_0 = pC0[2];
      rC3_0 = pC0[3];
      for (k = 56; k; k -= 2) {
        rA0 = *pA0;
        rB0 = *pB0;
        f64_I _t1 = _ia_mul_f64(rA0, rB0);
        rC0_0 = _ia_add_f64(rC0_0, _t1);
        rA1 = pA0[1 * 56];
        f64_I _t2 = _ia_mul_f64(rA1, rB0);
        rC1_0 = _ia_add_f64(rC1_0, _t2);
        rA2 = pA0[2 * 56];
        f64_I _t3 = _ia_mul_f64(rA2, rB0);
        rC2_0 = _ia_add_f64(rC2_0, _t3);
        rA3 = pA0[3 * 56];
        f64_I _t4 = _ia_mul_f64(rA3, rB0);
        rC3_0 = _ia_add_f64(rC3_0, _t4);
        rA0 = pA0[1 + 0 * 56];
        rB0 = pB0[1 + 0 * 56];
        f64_I _t5 = _ia_mul_f64(rA0, rB0);
        rC0_0 = _ia_add_f64(rC0_0, _t5);
        rA1 = pA0[1 + 1 * 56];
        f64_I _t6 = _ia_mul_f64(rA1, rB0);
        rC1_0 = _ia_add_f64(rC1_0, _t6);
        rA2 = pA0[1 + 2 * 56];
        f64_I _t7 = _ia_mul_f64(rA2, rB0);
        rC2_0 = _ia_add_f64(rC2_0, _t7);
        rA3 = pA0[1 + 3 * 56];
        f64_I _t8 = _ia_mul_f64(rA3, rB0);
        rC3_0 = _ia_add_f64(rC3_0, _t8);
        pA0 += 2;
        pB0 += 2;
      }
      *pC0 = rC0_0;
      pC0[1] = rC1_0;
      pC0[2] = rC2_0;
      pC0[3] = rC3_0;
      pC0 += 4;
      pA0 += incAm;
      pB0 += incBm;
    } while (pA0 != stM);
    pC0 += incCn;
    pA0 += incAn;
    pB0 += incBn;
  } while (pB0 != stN);
}
