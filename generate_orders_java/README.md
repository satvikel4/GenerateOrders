## To generate orders for some technique, run the bash script below:
### First the failed ones that all 3 methods need orders for
`bash generate_orders.sh modules.csv only`
`bash generate_orders.sh modules.csv intra`
`bash generate_orders.sh modules.csv inter`
### To be added for target pairs method
`bash generate_orders.sh modules.csv <name of method>`

- The script will go through each module listed in `modules.csv` and generate its orders based on the the method of generation that was passed. 
- The orders will be outputed to `outputs/` dir.  
- Original orders of the modules are in `original-orders/` directory.

### To generate orders for target pairs method
`bash generate_orders_static.sh module.csv

- The script will go through each module listed in `modules.csv` and generate its orders based on the target pairs method.
- The orders will be stored in .dtfixingtools_${short_sha}_static/orders under the corresponding module in the modules.csv.
