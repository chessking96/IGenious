/* fit/linear.c
 *
 * Copyright (C) 2000, 2007 Brian Gough
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */


/* Fit the data (x_i, y_i) to the linear relationship

   Y = c0 + c1 x

   returning,

   c0, c1  --  coefficients
   cov00, cov01, cov11  --  variance-covariance matrix of c0 and c1,
   sumsq   --   sum of squares of residuals

   This fit can be used in the case where the errors for the data are
   uknown, but assumed equal for all points. The resulting
   variance-covariance matrix estimates the error in the coefficients
   from the observed variance of the points around the best fit line.
*/


void gsl_fit_linear (long double *x, long double *y,
                long double *c0, long double *c1,
                long double *cov_00, long double *cov_01, long double *cov_11, long double *sumsq)
{
  int xstride = 1;
  int ystride = 1;
  int n = 100;


  long double m_x = 0;
  long double m_y = 0;
  long double m_dx2 = 0;
  long double m_dxdy = 0;

  int i;

  for (i = 0; i < n; i++)
    {
      m_x = m_x + (x[i * xstride] - m_x) / (i + 1.0);
      m_y = m_y + (y[i * ystride] - m_y) / (i + 1.0);
    }

  for (i = 0; i < n; i++)
    {
      long double dx = x[i * xstride] - m_x;
      long double dy = y[i * ystride] - m_y;

      m_dx2 = m_dx2 + (dx * dx - m_dx2) / (i + 1.0);
      m_dxdy = m_dxdy + (dx * dy - m_dxdy) / (i + 1.0);
    }

  /* In terms of y = a + b x */
  {
    long double s2 = 0;
    long double d2 = 0;
    long double b = m_dxdy / m_dx2;
    long double a = m_y - m_x * b;

    *c0 = a;
    *c1 = b;

    /* Compute chi^2 = \sum (y_i - (a + b * x_i))^2 */

    for (i = 0; i < n; i++)
      {
        long double dx = x[i * xstride] - m_x;
        long double dy = y[i * ystride] - m_y;
        long double d = dy - b * dx;
        d2 = d2 + d * d;
      }

    s2 = d2 / (n - 2.0);        /* chisq per degree of freedom */

    *cov_00 = s2 * (1.0 / n) * (1 + m_x * m_x / m_dx2);
    *cov_11 = s2 * 1.0 / (n * m_dx2);

    *cov_01 = s2 * (-m_x) / (n * m_dx2);

    *sumsq = d2;
  }

}
