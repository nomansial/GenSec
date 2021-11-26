
def after_scenario(context, scenario):
    """
        This method will execute only when a scenario has tag = regression
    """

    if "regression" in scenario.tags:
        print("API Executed. Please check Results")
