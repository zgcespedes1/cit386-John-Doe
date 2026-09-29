# ORDERS DATA QUALITY REPORT
========================================

- Source file rows processed (excluding header): 200
- Valid orders:                                  181
- Rejected rows:                                 19

 Total revenue (valid orders only): $48,490.04<br>  
 Average order value:                $267.90

----------------------------------------
Top 5 items by revenue
----------------------------------------
  Monitor      $11,016.00  (48 units)
  Printer      $6,164.35  (31 units)
  Router       $5,099.66  (34 units)
  Webcam       $3,827.00  (43 units)
  Dock         $3,480.00  (29 units)

----------------------------------------
Top 5 customers by spend
----------------------------------------
  Marcus Nair            $1,377.00 
  Gabriel Moreno         $1,147.50
  Teresa Munoz           $1,147.50  
  Oscar Rey              $1,007.94  
  Mateo Vidal            $994.25  

----------------------------------------
Rejected row breakdown (by primary reason)
----------------------------------------
    4  non-numeric/missing price
    3  blank row
    3  non-numeric quantity
    2  missing field
    2  negative quantity
    2  zero quantity
    2  missing customer name
    1  unexpected extra column

See rejected.csv for the full list of 19 rejected rows with line numbers and reasons.