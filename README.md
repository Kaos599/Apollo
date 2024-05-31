![](https://github.com/Kaos599/Apollo/assets/115716485/6967b98e-c7e7-43f4-a1ce-c1bf5d9fdde4)

# Apollo - Synthetic Data Generator

Apollo is a Python GUI application designed to simplify the complex process of generating random data based on fixed values. It allows users to generate various types of binary datasets, such as Yes/No type questions, by specifying probabilities. For example, if you want to generate data for "users that use our app daily" with a probability of 0.6, Apollo will ensure that 60% of the generated data reflects daily usage, while 40% does not. Additionally, you can create weighted options where multiple choices can be assigned different probabilities.

## Use Cases

Apollo can be utilized in various scenarios, including but not limited to:
- **Market Research**: Generate realistic survey data with custom probabilities for responses.
- **Software Testing**: Create test datasets for applications that require diverse input scenarios.
- **Machine Learning**: Produce synthetic datasets for training models, especially when real data is scarce or privacy is a concern.
- **Education**: Teach students about data generation and probabilistic distributions in a practical, hands-on manner.

## Installation

To get started with Apollo, you can either use the setup provided or manually install the required libraries and run the script.

### Using the Provided Setup

1. **Download and run the setup file**: [Setup Link]()
2. **Run the batch file**: This will automatically install all the necessary libraries for you.

### Manual Installation

If you prefer to manually install the dependencies and run the script, follow these steps:

1. **Install the required libraries**:
    ```bash
    pip install tkinter faker pandas
    ```

2. **Clone the repository and run the script**:
    ```bash
    git clone https://github.com/yourusername/apollo-synthetic-data-generator.git
    cd apollo-synthetic-data-generator
    python main.py
    ```

Alternatively, you can run the provided batch file to install the necessary libraries:
```bash
run.bat
```
## Libraries Required

Ensure you have the following Python libraries installed:

```python
from tkinter import ttk, messagebox, filedialog, simpledialog
from faker import Faker
import random
import pandas as pd
```

##Usage
Once installed, simply run the application. The user-friendly GUI will guide you through the process of generating synthetic data based on your specified probabilities and options.

##Thank You
Thank you for using Apollo! I hope it simplifies your data generation needs. If you have any questions or feedback, please feel free to reach out.
