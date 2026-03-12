import datetime
from trafik_info import weekly_report, monthly_report

if __name__ == "__main__":
    # Run the weekly report
    weekly_report()
    
    if datetime.datetime.today().day <= 7:
        # Run the monthly report
        monthly_report()
