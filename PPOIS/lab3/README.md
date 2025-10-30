# Warehouse management system

## Entities, Fields, Behaviors, Associations

Address 3 2  <br>
Employee 8 2 -> Person, Warehouse  <br>
Person 4 1 -> Address  <br>
Product 6 1 -> Category  <br>
BinType 8 0  
DeliveryStatus 5 0  
OrderStatus 6 0  
Category 5 0  
RouteStatus 4 0  
UOM 6 0  
VehicleType 4 1  
Customer 5 2 ->Order  
Delivery 8 4 ->Driver, Order, SalesAggregator, OrderStatus, DeliveryStatus  
OrderItem 2 1 -> Product  
Order 6 4 -> Customer, OrderItem, Delivery  
DeliveryReport 2 2 -> HRDepartment  
ExpirationReport 1 1 -> ExpirationChecker  
OrdersReport 2 3 -> Batch, Warehouse  
Report 4 1 -> Warehouse  
SalesReport 2 2 -> Warehouse, Aggregator  
StaffReport 2 2 -> Warehouse, HRDepartment  
StockReport 2 2 -> Warehouse  
Accountant 7 4 -> Address, HRDepartment  
Cleaner 6 1   
HRDepartment 15 16 -> WarehouseDirector, WarehouseManager, Storekeeper, Loader, SecurityGuard, Cleaner, Driver, OrderManager, Accountant, ExpirationChecker, LabelPrinter, ReceiptPrinter, PalletWrapper, Customer  
Driver 8 7 -> Vehicle, Delivery, Route  
ExpirationChecker 6 3 -> Batch, ExpiredBin, Location  
LabelPrinter 6 3 -> Batch, Product  
Loader 8 2 -> Batch, Location  
OrderManager 7 4 -> Customer, Order, Driver,SalesAggregator, Delivery  
PalletWrapper 6 1 -> Pallet   
ReceiptPrinter 6 1 -> Order  
SecurityGuard 6 3   
Storekeeper 7 5 -> Location, Product, Order, Batch  
WarehouseDirector 6 1 -> Manager  
WarehouseManager 9 8 -> Storekeeper, Loader, Location  
Batch 5 2 -> Product  
Bin 5 4 -> Batch  
Box 4 2   
ExpiredBin 4 3 -> Accountant, Warehouse, Batch, ExpirationChecker  
Location 2 6   
Pallet 4 2   
Shelf 3 1   
Stock 1 3 -> Batch  
Warehouse 4 4 -> ExpiredBin, Location, Product  
RoutePoint 4 1 -> Address   
Route 7 6 -> Driver, Vehicle, RoutePoint  
Vehicle 7 4 -> VehicleType  
SalesAggregator 1 3 -> OrderStatus, Order, Warehouse  
WarehouseChecker 1 1 -> Warehouse  
## Summary

Поля: 253 
Поведения: 132
Ассоциации: 83
