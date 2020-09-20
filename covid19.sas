
***********************************************************;
*  Author: Lovemore                                       *;
*    1) Get covid dataset fron ECDC website into SAS      *;
*                                                         *;
*                                                         *;
*                                                         *;
*    2) Check the contents of the dataset                 *;
*                                                         *;
*                                                         *;
*    3) Select South Afica Covid data only for further    *;
*       visualizations                                    *;
*                                                         *;
*    4) Format the dateRep variable and generate          *;
*       a new variable called Group based on specific     *;
*       month. Plot series plots for every month          *;
***********************************************************;

/*Macro*/
%let outpath = "C:\Users\Seanlove\Desktop\Data Science\SAS"

/* Fetch the file from the web site */
filename covid19 temp;
proc http
 url="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
 method="GET"
 out=covid19;
run;

/* Tell SAS to allow "nonstandard" names */
options validvarname=any;

/* import to a SAS data set */
proc import
  file=covid19
  out=work.covid19 replace
  dbms=csv;
run;

/*Checking the contents of the dataset*/
proc contents data=covid19;
run;


/*Selecting South Africa covid19 data, formating the date, dropping other variables*/
data covid19;
    set covid19;
    where countriesAndTerritories = "South_Afric";
    format  dateRep mmddyy10.;
    drop month year countryterritorycode continentExp countriesAndTerritories;
run;

/*Printing first 10 observations*/
proc print data=covid19(obs=10);
run;


/*Categorizing dates according to specific month*/
data covid19;
set covid19;
length group $10;
if daterep >='01sep2020'd and daterep <='30sep2020'd then group= "september";
else if daterep >='01aug2020'd and daterep<='31aug2020'd then group= "august";
else if daterep >='01jul2020'd and daterep <='31jul2020'd then group= "july";
else if daterep >='01jun2020'd and daterep <='30jun2020'd then group= "june";
else if daterep >='01may2020'd and daterep <='31may2020'd then group= "may";
else if daterep >='01apr2020'd and daterep <='30apr2020'd then group= "april";
else if daterep >='01mar2020'd and daterep <='31mar2020'd then group= "march";
else group='other';
run;

data covid19;
set covid19;
length newmonth $ 8;
select (group);
   when ('september') newmonth='7';
   when ('march') newmonth='1';
   when ('april') newmonth='2';
   when ('may') newmonth='3';
   when ('june') newmonth='4';
   when ('july') newmonth='5';
   when ('august') newmonth='6';
   otherwise;

end;

run;
/*Overall means of deaths and Cases per month*/
proc means data=covid19 mean median maxdec=2;
    class group;
    var deaths cases;
run;

/*Export document to pdf*/
options nodate;
ods pdf file="C:/Users/Seanlove/Desktop/Data Science/SAS/covid19.pdf"   startpage=no ;
ods noproctitle;

/*Series plot of Covid19 cases*/
ods graphics on / width=10.5in height=10.5in;
title "Series plot of Covid cases in South Africa";

proc sgplot data=covid19 noborder;
   styleattrs datacontrastcolors=(red green yellow black brown grey purple);
   series x=day y=cases / curvelabel curvelabelattrs=(size=12)
                           group=group lineattrs=(thickness=5);
						   label day = Day cases = Number of cases;
run;
title;
ods graphics on / scale=off;

/*Series plot of Covid19 deaths*/

ods graphics on / width=10.5in height=10.5in;
title "Series plot of Covid19 deaths in South Africa";

proc sgplot data=covid19 noborder;
   styleattrs datacontrastcolors=(red green yellow black brown grey purple);
   series x=day y=deaths / curvelabel curvelabelattrs=(size=12)
                           group=group lineattrs=(thickness=5);
						   label day = Day deaths = Number of deaths;
run;
title;
ods graphics on / scale=off;

ods pdf close;
