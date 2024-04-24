echo "Installing packages from init_script"
pip install refractio[snowflake]
pip install snowflake-snowpark-python==1.14.0
pip install snowflake-connector-python[pandas]==3.6.0
pip install xgboost
echo "Done with dependency installation!";
