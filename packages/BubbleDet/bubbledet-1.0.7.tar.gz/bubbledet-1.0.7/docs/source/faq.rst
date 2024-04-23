===========================================
FAQs
===========================================

- **Does BubbleDet include the zero mode factors automatically?**

    Yes! BubbleDet's function :py:data:`findDeterminat()` includes all zero mode factors.

- **Should I use the tree-level potential or the one-loop effective potential in BubbleDet?**

    For simple cases, such as were considered in Callan and Coleman's classic work\ :footcite:p:`Callan:1977pt` and in :doc:`our introduction <intro>`, the functional determinant arises from a saddle-point approximation of the path integral. So, the tree-level potential and *not* the one-loop potential should be used within both the bounce equations and the functional determinant. Using the one-loop effective potential would amount to double counting fluctuations, as well as an uncontrolled derivative expansion.

    However, when loop corrections are of leading-order importance for the potential, such as in thermal or radiatively-induced transitions, this question is more subtle\ :footcite:p:`Weinberg:1992ds`. In such cases, the relevant potential for both the bounce equation and the functional determinant is the tree-level potential for the nucleation scale effective field theory\ :footcite:p:`Gould:2021ccf`. The effective field theory approach avoids double counting and uncontrolled derivative expansions, and yields results which are real, gauge invariant and renormalisation scale invariant order-by-order.

- **For a thermal cosmological phase transition, what dimension should I use in BubbleDet?**

    In BubbleDet, the dimension :math:`d` should match the :math:`O(d)` symmetry of the background bubble. So, for a vacuum transition the dimension should be :math:`d=4`, while for a thermal transition the dimension should be :math:`d=3`.

- **What does the thermal flag do exactly?**

    Setting the :py:data:`thermal` flag equal to :py:data:`True` adds the dynamical prefactor, in the following approximation\ :footcite:p:`Affleck:1980ac`:

    .. math::
        &\texttt{findDeterminant(thermal=True)}= \\
        &\qquad\qquad
        \texttt{findDeterminant(thermal=False)}
        - \log\bigg(\frac{\sqrt{|\lambda_-|}}{2\pi} \bigg)

    where :math:`\lambda_-` is the negative eigenvalue of the fluctuations around the bubble. For more information on the dynamical prefactor, and the approximation we have adopted for it, see the BubbleDet paper\ :footcite:p:`Ekstedt:2023sqc`.

**********
References
**********

.. footbibliography::
