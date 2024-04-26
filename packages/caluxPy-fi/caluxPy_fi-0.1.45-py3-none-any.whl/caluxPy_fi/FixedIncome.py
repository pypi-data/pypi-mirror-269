import numpy as np, pandas as pd, math, time, logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox
from caluxPy_fi.Support import Support

class FixedIncome:

    #counter = 0
    
    def __init__(self, settlement_date, issuance_date, maturity_date, coupon, ytm, face_value, issuer, methodology, periodicity, payment_type, coupon_type, 
                 forward_date, amortization_start_date, amortization_periods, amortization_periodicity, amortizable_percentage, **kwargs):
        
        self.repo_margin = kwargs['repo_margin'] if 'repo_margin' in kwargs else ''
        self.repo_rate = kwargs['repo_rate'] if 'repo_rate' in kwargs else ''
        self.repo_tenure = kwargs['repo_tenure'] if 'repo_tenure' in kwargs else ''
        self.flr_rules = kwargs['flr_rules'] if 'flr_rules' in kwargs else ''
        self.flr_ratio = kwargs['flr_ratio'] if 'flr_ratio' in kwargs else ''
        self.date_format = kwargs['date_format'] if 'date_format' in kwargs else '%Y-%m-%d'
        self.multiple = kwargs['multiple'] if 'multiple' in kwargs else False
        self._lang = kwargs['lang'] if 'lang' in kwargs else 'eng'            
              
        #region ---> Logger
        
        desktop = Support.get_folder_path()
        
        _logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        _fileHandler = logging.FileHandler("{0}/{1}.log".format(desktop, 'fixed_income'), mode = 'w', encoding = 'utf-8')
        _fileHandler.setFormatter(_logFormatter)
        self._logger.addHandler(_fileHandler)

        #endregion ---> Logger
        
        #FixedIncome.counter += 1
        self._logger.info(f'Starting process with Security => Single Calculation') #{FixedIncome.counter}')
        self.results = {}

        self._start_time = time.perf_counter()

         #region ---> Tratamiento de las Fechas

        self.issuance_date = issuance_date
        try:
            if type(self.issuance_date) == str: self.issuance_date = datetime.strptime(issuance_date, self.date_format).date()
        except ValueError as e:
            self._logger.error(e)
        
        self.maturity_date = maturity_date
        try:
            if type(self.maturity_date) == str: self.maturity_date = datetime.strptime(maturity_date, self.date_format).date()
        except ValueError as e:
            self._logger.error(e)
        
        self.settlement_date = settlement_date
        try:
            if type(self.settlement_date) == str: self.settlement_date = datetime.strptime(settlement_date, self.date_format).date()
        except ValueError as e:
            self._logger.error(e)

        #endregion ---> Tratamiento de las Fechas
        
        self.issuer = issuer
        try:
            self.coupon = Support.rateConversion(rate = coupon)
        except Exception as e:
            self._logger.error(f'Error in Coupon Rate Conversion => {e}')
        try:
            self.ytm = Support.rateConversion(rate = ytm)
        except Exception as e:
            self._logger.error(f'Error in YTM Rate Conversion => {e}')
        
        self.payment_type = payment_type
        self.methodology = methodology
        self.face_value = float(face_value)
        
        try:
            if self.maturity_date >= self.settlement_date:
                try:
                    self.periodicity = Support.periodicityConversion(per = periodicity, mode = 'normal')
                except Exception as e:
                    self._logger.error(f'Error in Periodicity Conversion => {e}')
                self.a_maturity = True if periodicity in ['vencimiento', 'maturity'] else False

                self.coupon_type = coupon_type
                self._years_to_maturity = Support.years(self.issuance_date, self.maturity_date)

                self.residual_tenure = self.maturity_date - self.settlement_date #this is the remainder days to maturity
                self._total_coupons = self.periodicity * self._years_to_maturity #total amount of coupon payments of the security

                #Determinación del nper, esta parte determina la cantidad de flujos, si es a vencimiento será 1 sólo flujo
                try:
                    self._nper = math.trunc(Support.ln_nper(self.issuance_date, self.maturity_date, self.periodicity, self.coupon_type, self.a_maturity)) - 1
                except Exception as e: self._logger.error(f'Error determining nper => {e}')
                
                #The numeric periodicicy of the coupon payment, if it is to maturity it will always be equal to 1, but should not be equal to 0
                self._per = (12 / self.periodicity) if self.a_maturity == False else 1 
                
                #This is the expected maturity date of the security and should be the same as the provided, if not a discrepancy will be calculated and taken into account
                try:
                    self.expected_maturity = self.expectedMaturity(maturity_date = self.maturity_date, 
                                                                   issuance_date = self.issuance_date, 
                                                                   years_to_maturity = self._years_to_maturity,
                                                                   nper = self._per)
                except Exception as e: self._logger.error(f'Error calculating expected maturity => {e}')

                #This is the determination of the existence of a discrepancy between the maturity date and the expected maturity date
                if (self.maturity_date.day - self.issuance_date.day) != 0 or self.maturity_date != self.expected_maturity:
                    self._discrepancy = "Yes"
                else:
                    self._discrepancy = "No"
                    
                if self.coupon_type == 'normal':
                    self.forward_date = None
                elif coupon_type in ['fw1', 'fw2']:
                    #self.forward_date = datetime(self.maturity_date.year - math.trunc(self._years_to_maturity),self.maturity_date.month,self.maturity_date.day,0,0).date()
                    try:
                        self.forward_date = Support.get_date_years_ago(self.maturity_date, self._years_to_maturity)
                    except Exception as e:
                        self._logger.error(f'Error calculating a forward date => {e}')
                else:
                    self.forward_date = forward_date
                    if self.forward_date != '': 
                        try:
                            if type(forward_date) == str: self.forward_date = datetime.strptime(forward_date, self.date_format).date()
                        except ValueError as e:
                            self._logger.error(e)    
                    else:
                        self._logger.error('Forward date not specified!') 
                        raise Exception('Forward date not specified!')
                        
                #If the security if of bullet type then any attribute of amortizable is deleted to avoid incongruencies
                if self.payment_type == 'bullet':
                    self.amortization_start_date = None
                    self.amortization_periods = None
                    self.amortization_periodicity = None
                    self.amortizable_percentage = None
                else:
                    #If not bullet then all the attributes are kept and verified
                    self.amortization_start_date = amortization_start_date
                    self._logger.info(f'Amortization Date -> {self.amortization_start_date} Type => {type(self.amortization_start_date)}')
                    if self.amortization_start_date != '':
                        try:
                            if type(self.amortization_start_date) == str: self.amortization_start_date = datetime.strptime(self.amortization_start_date, self.date_format).date()
                            self._logger.info(f'Amortization Date -> {self.amortization_start_date} Type => {type(self.amortization_start_date)}')
                        except ValueError as e: self._logger.error(e)
                    else: 
                        self._logger.error('Amortization date not specified!') 
                        raise Exception('Amortization date not specified!')
                        
                    if amortization_periods != '':
                        self.amortization_periods = int(amortization_periods)
                    else:
                        self._logger.error('Amortization periods not specified!') 
                        raise Exception('Amortization periods not specified!')
                    
                    if amortization_periodicity != '':
                        try:
                            self.amortization_periodicity = Support.periodicityConversion(per = amortization_periodicity, mode = 'amortization')
                        except Exception as e: self._logger.error(f'Error converting amortization periodicity => {e}')
                    else:
                        self._logger.error('Amortization periodicity not specified!') 
                        raise Exception('Amortization periodicity not specified!')
                    
                    if amortizable_percentage != '':
                        try:
                            self.amortizable_percentage = Support.rateConversion(rate = amortizable_percentage)
                        except Exception as e: self._logger.error(f'Error converting amortization rate => {e}')
                    else:
                        self._logger.error('Amortization percentage not specified!') 
                        raise Exception('Amortization percentage not specified!')

                #Determination of the dates of coupon payments
                try:
                    self.coupon_dates = np.array(self.couponDates(nper = self._nper, 
                                                                  per = self._per, 
                                                                  issuance_date = self.issuance_date, 
                                                                  maturity_date = self.maturity_date, 
                                                                  coupon_type = self.coupon_type, 
                                                                  forward_date = self.forward_date,
                                                                  a_maturity = self.a_maturity))
                except Exception as e: self._logger.error(f'Error calculating coupon dates => {e}')
                #self._logger.info(f'Coupon Dates -> {self.coupon_dates} Type => {type(self.coupon_dates)}')
                #Iterates the list of coupon dates searching for which are greater than the settlement date and the first one matching is the current coupon
                self.current_coupon = (self.coupon_dates > self.settlement_date).nonzero()[0][0]
                try:
                    self.coupon_days, self.flow_num = self.couponDays_flowNum(nper = self._nper, 
                                                                              coupon_dates = self.coupon_dates, 
                                                                              issuance_date = self.issuance_date)
                except Exception as e: self._logger.error(f'Error calculating coupon days and flow numbers => {e}')
                
                try:
                    self.accumulated_days = self.accumulatedDays(methodology = self.methodology, 
                                                                 issuance_date = self.issuance_date, 
                                                                 fecha_liq = self.settlement_date, 
                                                                 current_coupon = self.current_coupon, 
                                                                 coupon_dates = self.coupon_dates)
                except Exception as e: self._logger.error(f'Error calculating accumulated days => {e}')
                
                try:
                    self.days_to_maturity = np.array(self.daysToMaturity(nper = self._nper, 
                                                                         coupon_days = self.coupon_days))
                except Exception as e: self._logger.error(f'Error calculating days to maturity => {e}')
                
                try:
                    self.calculation_basis = np.array(self.calculationBasis(methodology = self.methodology, 
                                                                            nper = self._nper, 
                                                                            coupon_dates = self.coupon_dates))
                except Exception as e: self._logger.error(f'Error calculating calculation basis => {e}')
                
                try:
                    self.w_coupon = self.wCoupon(methodology = self.methodology, 
                                                 coupon_days = self.coupon_days, 
                                                 current_coupon = self.current_coupon, 
                                                 accumulated_days = self.accumulated_days, 
                                                 periodicity = self.periodicity)
                except Exception as e: self._logger.error(f'Error calculating w coupon => {e}')
                    
                if self.payment_type in ['amortized', 'amortizado', 'pik']:
                    try:
                        self.notional_value, self.amortization_amount, self.adjusted_value, self.dates_results = self.amortizationModule(self.payment_type, self.amortization_start_date, self.maturity_date, 
                                                                                                                                         self.amortization_periods, self.amortization_periodicity, 
                                                                                                                                         self.amortizable_percentage, self.settlement_date, self.face_value, 
                                                                                                                                         self.coupon_dates, self.current_coupon, self._nper, self.periodicity)
                    except Exception as e: self._logger.error(f'Error in the amortization module => {e}')
                        
                else: self.notional_value = float(self.face_value)
                
                try:
                    self.gained_coupon = self.gainedCoupon(methodology = self.methodology, 
                                                           notional_value = self.notional_value, 
                                                           coupon = self.coupon, 
                                                           periodicity = self.periodicity, 
                                                           coupon_days = self.coupon_days, 
                                                           current_coupon = self.current_coupon, 
                                                           accumulated_days = self.accumulated_days, 
                                                           calculation_basis = self.calculation_basis)
                except Exception as e: self._logger.error(f'Error calculating gained coupon => {e}')
                    
                self.coupon_flow = []
                
                self._logger.info('SUCCESS: All necessary variables have been calculated! Proceeding with the calculation of the cash flows..')
                try:
                    if (self.payment_type in ['bullet']):
                        self.coupon_flow = np.array(self.bulletPaymentType(face_value = self.face_value, 
                                                                           coupon = self.coupon, 
                                                                           periodicity = self.periodicity, 
                                                                           nper = self._nper, 
                                                                           per = self._per, 
                                                                           methodology = self.methodology, 
                                                                           calculation_basis = self.calculation_basis, 
                                                                           coupon_days = self.coupon_days, 
                                                                           current_coupon = self.current_coupon))
                    elif (self.payment_type in ['amortized', 'amortizado']):
                        self.coupon_flow = np.array(self.amortizedPaymentType(methodology = self.methodology, 
                                                                              current_coupon = self.current_coupon, 
                                                                              dates_results = self.dates_results, 
                                                                              adjusted_value = self.adjusted_value, 
                                                                              coupon = self.coupon, 
                                                                              periodicity = self.periodicity, 
                                                                              amortization_amount = self.amortization_amount, 
                                                                              calculation_basis = self.calculation_basis, 
                                                                              coupon_days = self.coupon_days, 
                                                                              amortizable_percentage = self.amortizable_percentage, 
                                                                              nper = self._nper, 
                                                                              per = self._per))
                    elif (self.payment_type in ['pik']):
                        self.coupon_flow = np.array(self.pikPaymentType(methodology = self.methodology, 
                                                                        current_coupon = self.current_coupon, 
                                                                        dates_results = self.dates_results, 
                                                                        notional_value = self.notional_value, 
                                                                        coupon = self.coupon, 
                                                                        periodicity = self.periodicity, 
                                                                        calculation_basis = self.calculation_basis, 
                                                                        coupon_days = self.coupon_days, 
                                                                        nper = self._nper, 
                                                                        per = self._per))
                    self._logger.info('SUCCESS: Cash Flows calculated! Proceeding to calculate their respective present value..')
                except Exception as e: self._logger.error(f'Error calculating cashflows => {e}')
                
                try:   
                    valuation_results = self.presentValue(current_coupon = self.current_coupon, 
                                                          nper = self._nper, 
                                                          w_coupon = self.w_coupon, 
                                                          discrepancy = self._discrepancy, 
                                                          coupon_type = self.coupon_type, 
                                                          maturity_date = self.maturity_date, 
                                                          expected_maturity = self.expected_maturity, 
                                                          coupon_days = self.coupon_days, 
                                                          ytm = self.ytm, 
                                                          periodicity = self.periodicity, 
                                                          coupon_flow = self.coupon_flow, 
                                                          payment_type = self.payment_type, 
                                                          issuer = self.issuer, 
                                                          notional_value = self.notional_value, 
                                                          gained_coupon = self.gained_coupon)
                    self._logger.info('SUCCESS: Present value calculated! Proceeding with the results..')
                except Exception as e: self._logger.error(f'Error calculating present value of cashflows => {e}')
                
                self._final_time = time.perf_counter()
                self._process_time = self._final_time - self._start_time
                
                self.present_values = valuation_results[9]
                #Results of normal calculation
                self.results = self.create_results(valuation_results = valuation_results, status = True)
                self.results['status'] = 'Ok'
                #Otras operaciones
                try:
                    if self.repo_margin != '' and self.repo_rate != '' and self.repo_tenure != '':
                        self.repo_margin = float(Support.rateConversion(self.repo_margin))
                        self.repo_rate = float(Support.rateConversion(self.repo_rate))
                        self.repo_tenure = int(self.repo_tenure)
                        #print(self.repo_margin, self.repo_rate, self.repo_tenure)
                        resultado_repos = self.Repos(margin = self.repo_margin,
                                                     repo_rate = self.repo_rate,
                                                     repo_tenure = self.repo_tenure)
                        if self.multiple:
                            self.results['Valor Ida' if self._lang == 'esp' else 'Inflow'], self.results['Valor Vuelta' if self._lang == 'esp' else 'Outflow'] = resultado_repos
                        else:
                            self.results['valor_ida' if self._lang == 'esp' else 'one_way_value'], self.results['valor_vuelta' if self._lang == 'esp' else 'return_value'] = resultado_repos
                except Exception as e: 
                    self._logger.error(f'Error calculating repo => {e}')
                
                try:
                    if len(self.flr_rules) > 0 or self.flr_ratio != '':
                        self.available_amount, self.objective_notional = self.FLR(rules = self.flr_rules)
                        if self.multiple:
                            self.results['Disponible' if self._lang == 'esp' else 'Available'] = self.available_amount
                            self.results['Objetivo' if self._lang == 'esp' else 'Objective'] = self.objective_notional
                        else:
                            self.results['monto_disponible' if self._lang == 'esp' else 'available_amount'] = self.available_amount
                            self.results['monto_objetivo' if self._lang == 'esp' else 'objective_amount'] = self.objective_notional

                except Exception as e:
                    self._logger.error(f'Error calculating flr => {e}')
                    
                self._logger.info('SUCCESS: Results ready! Preparing the visualization..')

                values = {}
                est_flujos_exp = []
                flujos_exp = []
                present_values_export = []
                accumulated_days_export = []

                days = 0
                for i in range(len(self.flow_num)):
                    days += self.coupon_days[i]
                    accumulated_days_export.append(days)
                    if i < self.current_coupon:
                        est_flujos_exp.append('Vencido' if self._lang == 'esp' else 'Matured')
                        flujos_exp.append(0)
                        present_values_export.append(0)
                    else:
                        est_flujos_exp.append('Vigente' if self._lang == 'esp' else 'Active')
                        flujos_exp.append(self.coupon_flow[i - self.current_coupon])
                        present_values_export.append(self.present_values[i - self.current_coupon])

                values['Flujo' if self._lang == 'esp' else 'Flow'] = np.array(self.flow_num)
                values['Fecha Cupón' if self._lang == 'esp' else 'Coupon Date'] = np.array(self.coupon_dates)
                values['Días Cupón' if self._lang == 'esp' else 'Coupon Days'] = np.array(self.coupon_days)
                values['Días Acumulados' if self._lang == 'esp' else 'Accumulated Days'] = np.array(accumulated_days_export)
                values['Flujo Cupón' if self._lang == 'esp' else 'Coupon Flow'] = np.array(flujos_exp)
                values['Valor Presente' if self._lang == 'esp' else 'Present Value'] = np.array(present_values_export)
                values['Vigencia' if self._lang == 'esp' else 'Status'] = np.array(est_flujos_exp)

                self.df_results = pd.DataFrame(values)
                self._logger.info('SUCCESS: Results visualization ready! Exiting this procedure..')
            else:
                raise Exception('Security matured.')
        except Exception as e:
            self._logger.exception(e)
            self.results = self.create_results(valuation_results = [], status = False)
            self._logger.error('Título Vencido..' if self._lang == 'esp' else 'Matured Security..')
            self.results['status'] = 'Vencido' if self._lang == 'esp' else 'Matured'
            self._logger.error('Process cancelled because of an error')
        finally:
            self._logger.removeHandler(_fileHandler)
            _fileHandler.close()
    
    def amortizationDateValidation(self, coupon_dates, amortization_start_date, maturity_date, amortization_periods, amortization_periodicity):
        
        if (amortization_start_date in coupon_dates) == False:
            oldDate = amortization_start_date
            amortization_start_date = Support.closestDate(coupon_dates, amortization_start_date)
            prompt = '\n*ERROR! \nLa fecha de inicio de amortizaciones indicada no existe en los flujos de cupones, el programa procederá a buscar el cupon vigente más cercano.. ' + \
            '\n-Fecha Original: ' + str(oldDate.day) + '/' + str(oldDate.month) + '/' + str(oldDate.year) + \
            '\n-Fecha Nueva: ' + str(amortization_start_date.day) + '/' + str(amortization_start_date.month) + '/' + str(amortization_start_date.year)
            print(prompt , file = self.log)
            messagebox.showwarning('ValueError', prompt)
        fechaTest = amortization_start_date + relativedelta(months =+ ((amortization_periods - 1) * amortization_periodicity))
        if fechaTest > maturity_date:
            prompt = '\n*ERROR! \nLa fecha estimada de última amortización supera la fecha de vencimiento!' + \
                 '\n-Fecha de Vencimiento: ' + str(maturity_date.day) + '/' + str(maturity_date.month) + '/' + str(maturity_date.year) + \
                 '\n-Fecha estimada: ' + str(fechaTest.day) + '/' + str(fechaTest.month) + '/' + str(fechaTest.year)
            print(prompt, file = self.log)
            messagebox.showerror('ValueError', prompt)
            return amortization_start_date, False
        else: return amortization_start_date, True

    def expectedMaturity(self, maturity_date, issuance_date, years_to_maturity, nper):
        def check_months(maturity, issuance, nper):
            if maturity.month - issuance.month < 0:
                return maturity.month - issuance.month + nper
            elif maturity.month - issuance.month > 0:
                return maturity.month - issuance.month - nper
        #Determination of the expected maturity date
        if (check_months(maturity_date, issuance_date, nper)) != 0 or maturity_date.day != issuance_date.day:
            expected_maturity = date(issuance_date.year + math.trunc(years_to_maturity),issuance_date.month,issuance_date.day)
        else:
            expected_maturity = maturity_date
        return expected_maturity

    def couponDates(self, nper, per, issuance_date, maturity_date, coupon_type, forward_date, a_maturity = False): 
        #Determination of the dates in which coupons would be paid
        coupon_dates = []
        if a_maturity == False:
            i = 0
            while i <= nper:
                if i == 0:
                    if coupon_type == 'fw1':
                        coupon_dates.append((forward_date + relativedelta(months=+per)))
                    elif (coupon_type in ['fw2', 'fw3']):
                            coupon_dates.append(forward_date)
                    else:
                        coupon_dates.append((issuance_date + relativedelta(months=+per)))
                else:
                    if i == nper:
                        coupon_dates.append(maturity_date)
                    elif (coupon_type in ['fw2', 'fw3']):
                        coupon_dates.append((forward_date + relativedelta(months=+per * i)))
                    else:
                        coupon_dates.append((issuance_date + relativedelta(months=+per*(1+i))))   
                i += 1
        else:
           coupon_dates.append(maturity_date) 
        return coupon_dates

    def couponDays_flowNum(self, nper, coupon_dates, issuance_date): 
        #a) Determination of the days between each coupon
        #b) Determination of the flow number of the coupons
        coupon_days, flow_num = [], []
        i = 0
        while i <= nper:
            flow_num.append(i)
            if i == 0:
                coupon_days.append((coupon_dates[0] - issuance_date).days)
            else:
                coupon_days.append((coupon_dates[i] - coupon_dates[i - 1]).days)
            i += 1
        return coupon_days, flow_num

    def accumulatedDays(self, methodology, issuance_date, fecha_liq, current_coupon, coupon_dates): 
        #Determination of the accumulated days
        if (methodology != "isma-30-360") and current_coupon == 0:
            accumulated_days = (fecha_liq - issuance_date).days
        elif (methodology != "isma-30-360") and current_coupon != 0:
            accumulated_days = (fecha_liq - coupon_dates[current_coupon-1]).days
        elif (methodology == "isma-30-360") and current_coupon == 0:
            accumulated_days = (Support.days360(issuance_date,fecha_liq)).days
        elif (methodology == "isma-30-360") and current_coupon != 0:
            accumulated_days = (Support.days360(coupon_dates[current_coupon-1],fecha_liq))
        return accumulated_days

    def wCoupon(self, methodology, coupon_days, current_coupon, accumulated_days, periodicity): 
        #Determination of the w coupon
        if (methodology == 'isma-30-360'):
            w_coupon = ((360 / periodicity) - accumulated_days) / (360 / periodicity)
        else:
            w_coupon = (coupon_days[current_coupon] - accumulated_days) / coupon_days[current_coupon]
        return w_coupon

    def daysToMaturity(self, nper, coupon_days): 
        #Determination of the days between each coupon and the maturity date
        days_to_maturity = []
        i = 0
        while i <= nper:
            if i == 0:
                days_to_maturity.append(coupon_days[0])
            else:
                days_to_maturity.append(days_to_maturity[i - 1] + coupon_days[i])
            i += 1 
        return days_to_maturity

    def calculationBasis(self, methodology, nper, coupon_dates): 
        #Determination of the calculation basis
        calculation_basis = []
        i = 0
        while i <= nper:
            if (methodology == 'actual/365'):
                calculation_basis.append(365)
            elif (methodology in ['actual/360', 'isma-30-360']):
                calculation_basis.append(360)
            else:
                calculation_basis.append((coupon_dates[i] - (coupon_dates[i] - relativedelta(months=+12))).days)
            i += 1
        return calculation_basis

    #This module executes all calculations related to amortization including validations (should be included more validations and user inputs through streamlit)
    def amortizationModule(self, payment_type, amortization_start_date, maturity_date, amortization_periods, amortization_periodicity, amortizable_percentage, 
                           settlement_date, face_value, coupon_dates, current_coupon, nper, periodicity):
        #First this runs validations
        while True:
            amortization_start_date, validation = self.amortizationDateValidation(coupon_dates, amortization_start_date, maturity_date, amortization_periods, amortization_periodicity)
            if validation == False:
                while True:
                    seleccion = input('\nQue desea modificar para solucionar el error? ' + 
                              '\n1-Fecha de Inicio de las Amortizaciones' + 
                              '\n2-Periodicidad de las Amortizaciones' + 
                              '\n3-Cantidad de Amortizaciones' + 
                              '\nRespuesta: ')
                    if seleccion in ['1','2','3']:
                        if seleccion == '1': 
                            amortization_start_date = self.inputFecha('Fecha de Inicio de Amotizaciones')
                            break
                        elif seleccion == '2':
                            while True:
                                amortization_periodicity = Support.periodicityConversion(self.inputPrompt('periodicidad de amortizaciones', ['mensual','m','1','bimensual','b','2','trimestral','t','3','cuatrimestral','c','4','semestral','s','5','anual','a','6'], 3), mode = 'amortization')
                                if (amortization_periodicity == 12 / periodicity) or (amortization_periodicity == (12 / periodicity) * 2):
                                    break
                                else:
                                    prompt = 'Valor inválido: la periodicidad de las amortizaciones debe de ser igual o el doble de la periodicidad de pagos de cupones..'
                                    print(prompt, file = self.log)
                                    messagebox.showerror('ValueError', prompt)
                                    amortization_periodicity, 12 / periodicity
                                    continue
                            break
                        elif seleccion == '3':
                            amortization_periods = self.inputIntegers()
                            break
                    else:
                        prompt = 'Opción inválida, inténtelo de nuevo..'
                        print(prompt, file = self.log)
                        messagebox.showerror('InputError', prompt)
                        continue
                continue
            else: break

        #Determination of the dates in which the securities amortize
        amortization_amount = 0
        amortization_dates = []
        dates_results = []
        if (payment_type in ['amortized', 'amortizado', 'pik']):
            date_count = 0
            if amortization_start_date < settlement_date:
                date_count = 1
            i = 0
            while i <= int(amortization_periods) - 1:
                if i == 0:
                    amortization_dates.append(amortization_start_date)
                else:
                    amortization_dates.append(amortization_dates[i - 1] + relativedelta(months=+amortization_periodicity))
                    if amortization_dates[i] <= settlement_date:
                        date_count += 1
                i += 1
            amortization_dates = np.array(amortization_dates)
            i = 0
            posicion = 0
            while i <= np.count_nonzero(amortization_dates) - 1:
                posicion = np.where(coupon_dates == amortization_dates[i])[0]
                if posicion != 0: dates_results.append(posicion)
                i += 1
            amortization_amount = (face_value * amortizable_percentage) / amortization_periods
            dates_results = np.array(dates_results)
        #Calculating the Notional Value and the Adjusted Amounts
        previously_amortized = 0
        notional_value = 0
        adjusted_value = []
        if (payment_type in ['amortized', 'amortizado']):
            if amortization_periods > 0:
                if np.count_nonzero(dates_results) != date_count:
                    previously_amortized = amortization_amount * date_count
                notional_value = face_value - previously_amortized
            count = 0
            i = current_coupon
            while i <= nper:
                if np.where(dates_results == i)[0].size > 0:
                    count += 1
                    if count <= (amortization_periods - (amortization_periods - np.count_nonzero(dates_results))):
                        adjusted_value.append(notional_value - (amortization_amount * (count - 1)))
                    else:
                        adjusted_value.append(face_value)
                else:
                    adjusted_value.append(notional_value - (amortization_amount * count))
                i += 1
            adjusted_value = np.array(adjusted_value)

        return notional_value, amortization_amount, adjusted_value, dates_results

    def gainedCoupon(self, methodology, notional_value, coupon, periodicity, coupon_days, current_coupon, accumulated_days, calculation_basis): 
        #Calculates the running coupon or gained interest
        gained_coupon = 0
        if (methodology in ['icma']):
            gained_coupon = (notional_value * coupon / periodicity) / coupon_days[current_coupon] * accumulated_days
        elif (methodology in ['actual/actual', 'actual/365', 'actual/360']):
            gained_coupon = notional_value * coupon / calculation_basis[current_coupon] * accumulated_days
        elif (methodology in ['isma-30-360']):
            gained_coupon = notional_value * coupon / 360 * accumulated_days
        return gained_coupon

    def bulletPaymentType(self, face_value, coupon, periodicity, nper, per, methodology, calculation_basis, coupon_days, current_coupon):
        coupon_flow = []
        i = current_coupon
        while i <= nper:
            if (methodology in ['icma']):
                coupon_flow.append((face_value * coupon) / periodicity)
            elif (methodology in ['isma-30-360']):
                coupon_flow.append((face_value * coupon) / 12 * per)
            elif (methodology in ['actual/actual', 'actual/365', 'actual/360']):
                coupon_flow.append(face_value * coupon / calculation_basis[i] * coupon_days[i])
            if i == nper:
                coupon_flow[int(nper - current_coupon)] = face_value + coupon_flow[int(nper - current_coupon)]
            i += 1
        return coupon_flow
    
    def amortizedPaymentType(self, methodology, current_coupon, dates_results, adjusted_value, coupon, periodicity, amortization_amount, calculation_basis, coupon_days, amortizable_percentage, nper, per):
        i = current_coupon
        coupon_flow = []
        x = 0
        while i <= nper:
            if (methodology in ['icma']):
                if np.where(dates_results == i)[0].size > 0: #this coupon amortizes
                    coupon_flow.append((adjusted_value[x] * coupon / periodicity) + amortization_amount)
                else:#normal coupon
                    coupon_flow.append(adjusted_value[x] * coupon / periodicity)
            elif (methodology in ['isma-30-360']):
                if np.where(dates_results == i)[0].size > 0: #this coupon amortizes
                    coupon_flow.append(((adjusted_value[x] * coupon) / 12 * per) + amortization_amount)
                else: #normal coupon
                    coupon_flow.append((adjusted_value[x] * coupon) / 12 * per)
            elif (methodology in ['actual/actual', 'actual/365', 'actual/360']):
                if np.where(dates_results == i)[0].size > 0: #this coupon amortizes
                    coupon_flow.append((adjusted_value[x] * coupon / calculation_basis[i] * coupon_days[i]) + amortization_amount)
                else: #normal coupon
                    coupon_flow.append(adjusted_value[x] * coupon / calculation_basis[i] * coupon_days[i])
            if i == nper:
                if np.where(dates_results == i)[0].size > 0:
                    if amortizable_percentage == 1: #if amortizes 100%
                        coupon_flow[nper - current_coupon] = coupon_flow [x]
                    else: #if does not amortize 100%
                        coupon_flow[x] = adjusted_value[x] + coupon_flow[x] + amortization_amount
                else: 
                    coupon_flow[x] = adjusted_value[x] + coupon_flow[x]
            x += 1
            i += 1
        return coupon_flow
    
    def pikPaymentType(self, methodology, current_coupon, dates_results, notional_value, coupon, periodicity, calculation_basis, coupon_days, nper, per):
        i = current_coupon
        coupon_flow = []
        x = 0
        while i <= nper:
            if (methodology in ['icma']):
                if np.where(dates_results == i)[0].size > 0:
                    if i == current_coupon:
                        coupon_flow.append(notional_value + (notional_value * coupon / periodicity))
                    else:
                        coupon_flow.append(coupon_flow[x - 1] + (coupon_flow[x - 1] * coupon / periodicity))
                else:
                    coupon_flow.append(coupon_flow[x - 1] * coupon / periodicity)
            elif (methodology in ['isma-30-360']):
                if np.where(dates_results == i)[0].size > 0:
                    if i == current_coupon:
                        coupon_flow.append(notional_value + (notional_value * coupon) / 12 * per)
                    else:
                        coupon_flow.append(coupon_flow[x - 1] + ((coupon_flow[x - 1] * coupon) / 12 * per))
                else:
                    coupon_flow.append(coupon_flow[x - 1] * coupon / 12 * per)
            elif (methodology in ['actual/actual', 'actual/365', 'actual/360']):
                if np.where(dates_results == i)[0].size > 0:
                    if i == current_coupon:
                        coupon_flow.append(notional_value + (notional_value * coupon / calculation_basis[i] * coupon_days[i]))
                    else:
                        coupon_flow.append(coupon_flow[x - 1] + (coupon_flow[x - 1] * coupon / calculation_basis[i] * coupon_days[i]))
                else:
                    coupon_flow.append(coupon_flow[x - 1] * coupon / calculation_basis[i] * coupon_days[i])
            x += 1
            i += 1
        return coupon_flow

    def presentValue(self, current_coupon, nper, w_coupon, discrepancy, coupon_type, maturity_date, expected_maturity, coupon_days, ytm, periodicity, 
                             coupon_flow, payment_type, issuer, notional_value, gained_coupon): 
        #Calculation of the present value of the coupon payments
        fraction, factor = 0, 0
        preliminar_present_value, final_present_value = 0, 0
        clean_price, dirty_price, purchase_value = 0, 0, 0
        present_values, present_values_factor, values_cvx = [], [], []
        i = current_coupon
        while i <= nper:
            if (i + w_coupon - current_coupon) < 0:
                factor = 0
            else:
                if discrepancy == 'Yes' and i == nper:
                    if (coupon_type in ['fw1', 'fw2']):
                        fraction = 0
                    else:
                        fraction = ((maturity_date - expected_maturity).days) / coupon_days[nper - 1]
                factor = (i + w_coupon - current_coupon) + fraction
            if issuer in ['Hacienda', 'hacienda'] and i == current_coupon:
                if current_coupon == nper:
                    present_values.append((coupon_flow[i - current_coupon] / (1 + (ytm / periodicity)) ** factor) -
                    (coupon_flow[i - current_coupon] * (1 - w_coupon)) + (notional_value / (1 + (ytm / periodicity)) ** factor))
                else:
                    present_values.append((coupon_flow[i - current_coupon] / (1 + (ytm / periodicity)) ** factor) -
                    (coupon_flow[i - current_coupon] * (1 - w_coupon)))
            else:
                present_values.append(coupon_flow[i - current_coupon] / (1 + ytm / periodicity) ** factor)
            present_values_factor.append(present_values[i - current_coupon] * factor)
            values_cvx.append(present_values[i - current_coupon] * (factor ** 2 + factor))
            i += 1
        #Conversion to numpy arrays
        present_values = np.array(present_values)
        present_values_factor = np.array(present_values_factor) #necessary for the duration
        values_cvx = np.array(values_cvx) #necessary for convexity
        #Depending on the payment type, changes the present value of the security
        if (payment_type in ['pik']):
            preliminar_present_value = present_values [-1]
        else:
            preliminar_present_value = present_values.sum()
        #Pricing outputs and final values depending on the issuer
        if issuer not in ['Hacienda', 'hacienda']:
            final_present_value = preliminar_present_value
            dirty_price = round(final_present_value / notional_value,10)
            clean_price = round((final_present_value - gained_coupon) / notional_value,10)
            purchase_value = round(final_present_value - gained_coupon, 2)
            final_present_value = round(final_present_value,2)
        else:
            clean_price = round(preliminar_present_value / notional_value,6)
            final_present_value = round((notional_value * clean_price) + gained_coupon, 2)
            dirty_price = round(final_present_value / notional_value,6)
            purchase_value = round(notional_value * clean_price,2)
        duration = (np.sum(present_values_factor) / preliminar_present_value) / periodicity
        modified_duration = duration / (1 + (ytm / periodicity))
        dv01 = dirty_price * (modified_duration / 100) * notional_value / 100
        convexity = np.sum(values_cvx) / (1 + (ytm / periodicity)) ** 2 / preliminar_present_value / periodicity ** 2
        return final_present_value, dirty_price, purchase_value, clean_price, duration, modified_duration, dv01, convexity, preliminar_present_value, present_values

    def Repos(self, margin, repo_rate, repo_tenure):
        count = -1
        gained_coupon = 0
        flow_dates = {}
        error = 0
        
        settlement_date = self.settlement_date
        one_way_value, return_value = 0, 0
        if self._lang == 'eng':
            try:
                if self.multiple:
                    present_value = self.results['Preliminar Present Value']
                else:
                    present_value = self.results['preliminar_present_value']
            except Exception:
                error += 1
                
        elif self._lang == 'esp':
            try:
                if self.multiple:
                    present_value = self.results['Valor Presente Preliminar']
                else:
                    present_value = self.results['valor_presente_preliminar']
            except Exception:
                error += 1

        if error > 0: return None, None
        
        coupon_dates = self.coupon_dates
        coupon_flows = self.coupon_flow
        repo_maturity = settlement_date + relativedelta(days =+ repo_tenure)
        if repo_maturity >= self.maturity_date:
            prompt = 'ERROR: Security matures before the repo..'
            return None, None

        for date in coupon_dates:
            if date > settlement_date:
                count += 1
                flow_dates[date] = coupon_flows[count]

        for key, value in flow_dates.items():
            if key == repo_maturity:
                flow_dates[key] = value - self.notional_value
        
        for date in coupon_dates:
            if date > settlement_date and date < repo_maturity:
                gained_coupon += flow_dates[date]

        adjusted_present_value = present_value - gained_coupon
        one_way_value = adjusted_present_value * ( 1 - margin)
        return_value = one_way_value * (1 + repo_rate / 365 * repo_tenure)

        return one_way_value, return_value

    def FLR(self, rules: dict):
        asked_amount = self.face_value #this as a rule makes more sense
        available_amount, objective_notional = 0, 0
        if self.flr_ratio == '':
            rule = rules['gov'] if self.issuer.lower() in ['bcrd', 'hacienda'] else rules['other']
        else:
            rule = self.flr_ratio
        rule = float(rule)  
        
        if self.multiple:
            present_value = self.results['Valor Presente Preliminar' if self._lang == 'esp' else 'Preliminar Present Value']
        else:
            present_value = self.results['valor_presente_preliminar' if self._lang == 'esp' else 'preliminar_present_value']

        try:
            dirty_price = present_value / self.notional_value
        except Exception as e:
            self._logger.error(f'Error calculating dirty price => {e}')
        available_amount = present_value / rule
        
        try:
            objective_notional = Support.solver(self.notional_value, dirty_price, asked_amount, rule) #se pudiera hacer el round a -4.. ponderar
        except Exception as e:
            self._logger.error(f'Error in the optimization => {e}')
            
        return available_amount, objective_notional

    def create_results(self, valuation_results, status):
        results = {}
        if self.multiple == False:
            results['valor_presente' if self._lang == 'esp' else 'present_value'] = valuation_results[0] if status else None
            results['precio' if self._lang == 'esp' else 'price'] = valuation_results[1] if status else None
            results['valor_compra' if self._lang == 'esp' else 'purchase_value'] = valuation_results[2] if status else None
            results['precio_limpio' if self._lang == 'esp' else 'clean_price'] = valuation_results[3] if status else None
            results['duracion' if self._lang == 'esp' else 'duration'] = valuation_results[4] if status else None
            results['duracion_modificada' if self._lang == 'esp' else 'modified_duration'] = valuation_results[5] if status else None
            results['dv01'] = valuation_results[6] if status else None
            results['convexidad' if self._lang == 'esp' else 'convexity'] = valuation_results[7] if status else None
            results['valor_presente_preliminar' if self._lang == 'esp' else 'preliminar_present_value'] = valuation_results[8] if status else None
            results['tiempo_calculo' if self._lang == 'esp' else 'process_time'] = self._process_time if status else None
        elif self.multiple == True:
            results['Emisor' if self._lang == 'esp' else 'Issuer'] = self.issuer
            results['Fecha Vencimiento' if self._lang == 'esp' else 'Maturity Date'] = self.maturity_date
            results['Monto' if self._lang == 'esp' else 'Face Value'] = self.face_value
            results['Rendimiento' if self._lang == 'esp' else 'Yield'] = self.ytm
            results['Cupón Corrido' if self._lang == 'esp' else 'Running Coupon'] = self.gained_coupon if status else None
            results['Valor Presente' if self._lang == 'esp' else 'Present Value'] = valuation_results[0] if status else None
            results['Precio Sucio' if self._lang == 'esp' else 'Dirty Price'] = valuation_results[1] if status else None
            results['Valor Compra' if self._lang == 'esp' else 'Purchase Value'] = valuation_results[2] if status else None
            results['Precio Limpio' if self._lang == 'esp' else 'Clean Price'] = valuation_results[3] if status else None
            results['Duracion' if self._lang == 'esp' else 'Duration'] = valuation_results[4] if status else None
            results['Duracion Modificada' if self._lang == 'esp' else 'Modified Duration'] = valuation_results[5]  if status else None
            results['DV01'] = valuation_results[6] if status else None
            results['Convexidad' if self._lang == 'esp' else 'Convexity'] = valuation_results[7] if status else None
            results['Valor Presente Preliminar' if self._lang == 'esp' else 'Preliminar Present Value'] = valuation_results[8] if status else None
            results['Tiempo de Cálculo' if self._lang == 'esp' else 'Process Time'] = self._process_time if status else None
        return results
     
    def get_results(self):
            
        return self.results

    def __str__(self):
        try:
            if self._lang == 'eng':
                if self.settlement_date <= self.maturity_date:
                    return(f'\nSecurity Summary:\n \n \
Issuance Date: {self.issuance_date}\n \
Maturity Date: {self.maturity_date}\n \
Coupon Rate: {self.coupon}\n \
Yield to Maturity: {self.ytm}\n \
Payment Type: {self.payment_type}\n \
Coupon Type: {self.coupon_type}\n \
Periodicity: {self.periodicity}\n \
Methodology (basis): {self.methodology}\n \
Face Value: {self.face_value}\n \
Present Value: {self.results['present_value']}\n \
Price: {self.results['price']}\n \
Purchase Value: {self.results['purchase_value']}\n \
Clean Price: {self.results['clean_price']}\n \
Duration: {self.results['duration']}\n \
Modified Duration: {self.results['modified_duration']}\n \
DV01: {self.results['dv01']}\n \
Convexity: {self.results['convexity']}\n \
Preliminar Present Value: {self.results['preliminar_present_value']}\n \
Process Time: {self.results['process_time']}\n')
                else:
                    return f'Security matured by: {self.maturity_date - self.settlement_date} days'
            elif self._lang == 'esp':
                if self.settlement_date <= self.maturity_date:
                    return(f'\nResumen del Título:\n \n \
Fecha de Emisión: {self.issuance_date}\n \
Fecha de Vencimiento: {self.maturity_date}\n \
Tasa Cupón: {self.coupon}\n \
Rendimiento: {self.ytm}\n \
Tipo de Pago: {self.payment_type}\n \
Tipo de Cupón: {self.coupon_type}\n \
Periodicidad: {self.periodicity}\n \
Metodología (basis): {self.methodology}\n \
Monto: {self.face_value}\n \
Valor Presente: {self.results['valor_presente']}\n \
Precio: {self.results['precio']}\n \
Valor de Compra: {self.results['valor_compra']}\n \
Precio Limpio: {self.results['precio_limpio']}\n \
Duración: {self.results['duracion']}\n \
Duración Modificada: {self.results['duracion_modificada']}\n \
DV01: {self.results['dv01']}\n \
Convexidad: {self.results['convexidad']}\n \
Valor Presente Preliminar: {self.results['valor_presente_preliminar']}\n \
Tiempo de Cálculo: {self.results['tiempo_calculo']}\n')
                else:
                    return f'Título vencido por: {self.maturity_date - self.settlement_date} días'
        except Exception:
            return f'Security error!'


class Letras:
    def __init__(self, settlement_date, maturity_date, ytm, face_value, repo_margin = '', repo_rate = '', repo_tenure = '', date_format = '', multiple = False) -> None:
        self.settlement_date = settlement_date
        self.maturity_date = maturity_date
        self.ytm = ytm
        self.face_value = face_value
        self.repo_margin = repo_margin
        self.repo_rate = repo_rate
        self.repo_tenure = repo_tenure
        self.date_format = date_format
        self.multiple = multiple

        self.days_to_maturity = self.maturity_date - self.settlement_date
        self.price = 360 / (360 + self.ytm * self.days_to_maturity)
        self.purchase_value = self.face_value * self.price
        self.discount = self.face_value - self.purchase_value