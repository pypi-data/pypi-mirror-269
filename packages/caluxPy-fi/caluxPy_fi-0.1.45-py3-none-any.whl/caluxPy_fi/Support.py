import re, math
from scipy.optimize import minimize
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import logging, os, pathlib

class Support ():

    def rateConversion(rate):
        if type(rate) == str and re.search('%',rate)!=None:
            return float(rate.replace('%',''))/100
        elif float(rate) > 1:
            return float(rate) / 100
        else:
            return float(rate)
    
    def periodicityConversion(per, mode):
        if per in ['anual', 'a', '6', 'vencimiento', 'v', '7']:
            if mode == 'normal':
                return 1
            elif mode == 'amortization':
                return 12
        elif per in ['semestral', 's','5']:
            if mode == 'normal':
                return 2
            elif mode == 'amortization':
                return 6
        elif per in ['cuatrimestral', 'c', '4']:
            if mode == 'normal':
                return 3
            elif mode == 'amortization':
                return 4
        elif per in ['trimestral', 't', '3']:
            if mode == 'normal':
                return 4
            elif mode == 'amortization':
                return 3
        elif per in ['bimensual', 'b', '2']:
            if mode == 'normal':
                return 6
            elif mode == 'amortization':
                return 2
        elif per in ['mensual', 'm', '1']:
            if mode == 'normal':
                return 12
            elif mode == 'amortization':
                return 1  

    def monthSelection(mes):
        if mes == 1:
            return 'enero'
        if mes == 2:
            return 'febrero'
        if mes == 3:
            return 'marzo'
        if mes == 4:
            return 'abril'
        if mes == 5:
            return 'mayo'
        if mes == 6:
            return 'junio'
        if mes == 7:
            return 'julio'
        if mes == 8:
            return 'agosto'
        if mes == 9:
            return 'septiembre'
        if mes == 10:
            return 'octubre'
        if mes == 11:
            return 'noviembre'
        if mes == 12:
            return 'diciembre'
    
    def years(issuance_date, maturity_date):

        def is_leap_year(year):
            """Check if a year is a leap year."""
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        
        def days_in_year(year):
            """Return the number of days in a year, considering leap years."""
            return 366 if is_leap_year(year) else 365
        
        # Calculate the initial year difference
        year_difference = maturity_date.year - issuance_date.year

        # Adjust the start date by the year difference to see if we've gone too far
        adjusted_date = issuance_date.replace(year=issuance_date.year + year_difference)
        
        # If we've gone too far, decrease the year difference
        if adjusted_date > maturity_date:
            year_difference -= 1
            adjusted_date = issuance_date.replace(year=issuance_date.year + year_difference)
        
        # Calculate the remaining days after the last full year
        remaining_days = (maturity_date - adjusted_date).days
        
        # Calculate the fraction of the year for the remaining days
        # This requires knowing if the last part of the period is a leap year
        final_year_days = days_in_year(adjusted_date.year)
        year_fraction = remaining_days / final_year_days
        precise_year_difference = year_difference + year_fraction
    
        '''# Directly calculate total days difference
        total_days = (maturity_date - issuance_date).days
        
        # Calculate initial year difference
        year_difference = maturity_date.year - issuance_date.year
        
        # Adjust for the case where the end date hasn't yet reached the start date's month and day
        if maturity_date.month < issuance_date.month or (maturity_date.month == issuance_date.month and maturity_date.day < issuance_date.day):
            year_difference -= 1

        # Check for leap year adjustments
        leap_day_count = 0
        if issuance_date <= datetime(issuance_date.year, 2, 29) <= maturity_date:
            leap_day_count += 1
        if issuance_date.year != maturity_date.year and issuance_date <= datetime(maturity_date.year, 2, 29) <= maturity_date:
            leap_day_count += 1

        # Calculate the precise difference in years, considering leap years
        precise_year_difference = year_difference + (total_days - leap_day_count) / 365.25'''

        '''def is_leap_year(year):
            """Check if a year is a leap year."""
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        
        # Calculate the total number of days between the two dates
        total_days = (maturity_date - issuance_date).days
        
        # Count leap days in the range
        leap_days = sum(1 for year in range(issuance_date.year, maturity_date.year + 1)
                        if is_leap_year(year)
                        and (datetime(year, 2, 29).date() >= issuance_date)
                        and (datetime(year, 2, 29).date() < maturity_date))
        
        # Calculate the average number of days per year considering leap days
        years_difference = maturity_date.year - issuance_date.year
        average_days_per_year = (years_difference * 365 + leap_days) / years_difference if years_difference else 0
        
        # Calculate the precise difference in years
        precise_year_difference = total_days / average_days_per_year if average_days_per_year else 0'''
        '''if maturity_date.year % 4 == 0:
            divisor_año = 366
        else:
            divisor_año = 365
        dif_años = relativedelta(maturity_date, issuance_date).years
        dif_meses = relativedelta(maturity_date, issuance_date).months / 12
        dif_dias = relativedelta(maturity_date, issuance_date).days / divisor_año
        return dif_años + dif_meses + dif_dias'''
        return precise_year_difference

    def get_date_years_ago(end_date, year_difference):
        def is_leap_year(year):
            """Check if a year is a leap year."""
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        # Calculate the start year by subtracting the truncated year difference from the end year
        start_year = end_date.year - math.trunc(year_difference)
        
        # Handle the case where subtracting the years results in a date before February 29 in a leap year
        if end_date.month == 2 and end_date.day == 29 and not is_leap_year(start_year):
            # Adjust the start date to February 28 if the start year is not a leap year
            start_date = datetime(start_year, end_date.month, 28)
        else:
            # Ensure the new date does not exceed the month's day limit
            try:
                start_date = datetime(start_year, end_date.month, end_date.day)
            except ValueError:
                # Adjust for cases like April 31st; set to the last day of the month
                start_date = datetime(start_year, end_date.month + 1, 1) - timedelta(days=1)
        return start_date.date()
    
    def ln_nper(issuance, maturity, fper, type, a_maturity = False):
        if a_maturity == False:
            rel_nper = (relativedelta(maturity, issuance).years * 12 / (12 / fper)) + (relativedelta(maturity, issuance).months / (12 / fper))
            if (rel_nper - math.trunc(rel_nper)) > 0: 
                if (type == 'fw2'): 
                    rel_nper += 1
        else:
            rel_nper = 1
        return rel_nper

    def days360(start_date,end_date,method_eu=False):
        
        start_day = start_date.day
        start_month = start_date.month
        start_year = start_date.year
        end_day = end_date.day
        end_month = end_date.month
        end_year = end_date.year
    
        if (
            start_day == 31 or
            (
                method_eu is False and
                start_month == 2 and (
                    start_day == 29 or (
                        start_day == 28 and
                        start_date.is_leap_year is False
                    )
                )
            )
        ):
            start_day = 30
    
        if end_day == 31:
            if method_eu is False and start_day != 30:
                end_day = 1
                if end_month == 12:
                    end_year += 1
                    end_month = 1
                else:
                    end_month += 1 
            else:
                end_day = 30
        return (
            end_day + end_month * 30 + end_year * 360 - 
            start_day - start_month * 30 - start_year * 360)

    def solver(v1, v2, v3, v4):

        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'cMult'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        objetivo = v4
        # Define the objective function
        def objective (x):
            x1 = x[0] #valor nocional
            x2 = x[1] #valor presente
            x3 = x[2] #monto solicitado
            x4 = x[3] #ratio
            return (x1 * x2) / x3

        # Define the constraint function(s)
        def constraint1 (x):
            return ((x[0] * x[1]) / x[2]) - x[3] #equality
        
        # Define the initial guess for the variables
        x0 = [v1, v2, v3, v4]
        logger.info(f'Valor inicial de la función objetivo: {objective(x0)}')

        # Define the bounds for the decision variables
        b1 = (0, None) #variable
        b2 = (v2, v2) #fixed
        b3 = (v3, v3) #fixed
        b4 = (v4, v4) #fixed
        bnds = (b1, b2, b3, b4) #grouping bounds
        con1 = {'type': 'eq', 'fun': constraint1} #set the constraint with type of equality
        cons = [con1] #grouping constraints

        # Define the termination tolerance
        tolerance = 1e-100

        sol = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons, tol = tolerance)

        if abs(sol.fun - objetivo) <= tolerance and sol.success == True and sol.fun > 0:
            t1 = sol.x[0]
            t2 = sol.x[1]
            t3 = sol.x[2]
            test = (t1 * t2) / t3
            #logger.info(f'Residual: {test - v4}')
            #logger.info(f'Resultados Solver: {sol}')
            logger.removeHandler(fileHandler)
            fileHandler.close()
            #logging.shutdown()
            return sol.x[0]
        else:
            logger.warning("No solution found within the desired tolerance range.")
            logger.removeHandler(fileHandler)
            fileHandler.close()
            #logging.shutdown()
            return 0
            
    def closestDate(fechas, buscada):

        return min(fecha for fecha in fechas if fecha >= buscada)
    
    def get_folder_path():
        # Get the path to the user's home directory
        home = pathlib.Path.home()

        # Construct the path to the desktop
        desktop = home / "Desktop"

        # Check if the desktop path exists; this is useful for OS's with different desktop paths
        if not desktop.exists():
            # Alternative approach for systems where the desktop might have a different name
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        if not os.path.exists(desktop):
            folder_path = os.path.join(home, 'cxfiLogs')
        else:
            folder_path = os.path.join(desktop, 'cxfiLogs')
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
                
        return folder_path