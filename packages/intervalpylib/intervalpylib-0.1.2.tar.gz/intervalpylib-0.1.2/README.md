## Project title
IntervalPyLib implments the necessary functionality to solve the systems of equations describing a robot's workspace area.

## Decription
The robot has a lot of unknown variables, such as velocity, different angles, lengths and more importantly its position.
Based on these variables, a kinematic system of equations is constructed that restricts the robot's workspace area.
This package allows for easy solving and visualization of such equations.

## How to install
This package can be installed using python's `pip`:
```bash
python3 -m pip install intervalpylib
```

## How to use
First of all, import that package:
```bash
import intervalpylib as ival_utils
``` 
or 
```bash
from intervalpylib import <necessary class>
```

Inside the package, there are 3 main classes that provide necessary functionality:

1. SymbolicEquationSolver, provides the functionality for algebraic system manipulations needed for other classes
2. AreaCalculator, contains the functions/methods that allow to visualize the solution, as well as contain the analytically calculated robot areas for some known configurations
3. Solver, an abstract class that sets the interface which custom solvers need to respect

As an example, `KrawczykSolver` is included in the package (it implements the interval Krawczyk operator)

Example usage is included in the `example.py`

## License
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
