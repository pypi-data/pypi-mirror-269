import sympy


class SymbolicEquationSolver:
    """System of equations class that allows for algebraic manipulations
    """
    def __init__(self, name, params):
        """Constructor

        Args:
            name (string): The name of the system
            params (dict): Parameters for the preconfigured system
        """
        if name == "2-RPR":
            self._f, self._u, self._v = self.__symbolic_2rpr_func(*params)
        elif name == "3-RPR":
            self._f, self._u, self._v = self.__symbolic_3rpr_func(*params)
        elif name == "custom":
            assert len(params) >= 3
            self._f, self._u, self._v = params[0], params[1], params[2]
        
        self._f_lam = None
        self._df_lam = None
    
    def __symbolic_2rpr_func(self, d=8):
        """Creates the symbols for 2-RPR system

        Args:
            d (float, optional): distance between the stationary points. Defaults to 8.

        Returns:
            Tuple[Matrix, List[symbol], List[symbol]]: the system's matrix, the list of known variables and checking variables
        """
        v = sympy.symbols("v1, v2")
        u = sympy.symbols("u1, u2")
        f = sympy.Matrix(
            [
                [v[0] ** 2 - (u[0] + 0.5 * d) ** 2 - u[1] ** 2],
                [v[1] ** 2 - (u[0] - 0.5 * d) ** 2 - u[1] ** 2],
            ]
        )
        return f, u, v

    def __symbolic_3rpr_func(self, x_c, y_c):
        """Creates the symbols for 3-RPR system

        Args:
            x_c (List[float], optional): the list of x-coordinates of the stationary points
            y_c (List[float], optional): the list of y-coordinates of the stationary points

        Returns:
            Tuple[Matrix, List[symbol], List[symbol]]: the system's matrix, the list of known variables and checking variables
        """
        v = sympy.symbols("v1, v2, v3")
        u = sympy.symbols("u1, u2")
        f = sympy.Matrix(
            [
                [-v[0] ** 2 + (u[0] - x_c[0]) ** 2 + (u[1] - y_c[0]) ** 2],
                [-v[1] ** 2 + (u[0] - x_c[1]) ** 2 + (u[1] - y_c[1]) ** 2],
                [-v[2] ** 2 + (u[0] - x_c[2]) ** 2 + (u[1] - y_c[2]) ** 2],
            ]
        )
        return f, u, v
    
    def __derive_matrix(self, f, x):
        """Functino for calculating partial derivatives of matrix g

        Args:
            f (Matrix): array to be derived
            x (List[symbol]): variables for derivative

        Returns:
            Matrix: derived matrix
        """
        g_v_all = []
        for i in range(len(x)):
            g_v_all.append(sympy.diff(f, x[i]))  # Calculate derivative of G with respect to v
        gv = sympy.Matrix()
        for i in range(len(g_v_all)):
            gv = sympy.Matrix([gv, g_v_all[i]])
        gv = gv.reshape(f.shape[0], len(x)).T
        return gv
    
    @property
    def f(self):
        """F property

        Returns:
            Matrix: system's matrix
        """
        return self._f
    
    @property
    def u(self):
        """U property

        Returns:
            Matrix: system's fixed variables
        """
        return self._u
    
    @property
    def v(self):
        """V property

        Returns:
            Matrix: system's checking variables
        """
        return self._v

    @property
    def f_num_lam(self):
        """F_num_lam property

        Returns:
            Matrix: system's matrix lambdified function
        """
        if self._f_lam is None:
            self._f_lam = sympy.lambdify([self.u, self.v], self.f)
        return self._f_lam
    
    @property
    def df_num_lam(self):
        """Df_num_lam property

        Returns:
            Matrix: system's derivative matrix lambdified function
        """
        if self._df_lam is None:
            df = self.__derive_matrix(self.f, self.v)
            self._df_lam = sympy.lambdify([self.u, self.v], df)
        return self._df_lam
    
if __name__ == "__main__":
    two_rpr = SymbolicEquationSolver("2-RPR", [8])
    print(two_rpr.f, two_rpr.u, two_rpr.v)
