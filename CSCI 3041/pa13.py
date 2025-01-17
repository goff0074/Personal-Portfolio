import traceback

#Takes as input two parameters:

# price_list is a list of Order objects that represents today's cost for a
#  single order of various quantities of chicken wings.  You can assume that
#  price_list is always in order from lowest quantity of wings to highest,
#  but there is no guarantee that every integer between 1 and num_wings is
#  a valid order size

# num_wings is an integer, representing the minimum number of chicken wings
#  you need to order today to send the correct message to the shadow
#  organization

# Returns a list Order objects representing the set of wing orders with the
#  minimum total cost that contain at least num_wings wings.
def optimize_wings(price_list, num_wings):
    price_of_orders = [Order(0, 0)] #A list to store every single price of the orders possible
    current_wing_index = 0 #keeps track of the current order of wings
    for order_price in price_list: #loop thorugh every order price in the price list
        price_of_orders.extend([order_price] * (order_price.wings - current_wing_index))
        current_wing_index = order_price.wings # Add the order price for each of the orders, for every order/wings necessary
    price_of_orders.extend([Order(0, float('inf'))] * (num_wings - current_wing_index))
    current_wing_index = num_wings #in case there are leftover wings, you need to make their price very high

    optimal_wing_prices = [0] * (num_wings + 1)
    optimal_order_split = [0] * (num_wings + 1) #create lists for the optimal wing prices, and the dynamic programming splits
    for j in range(1, num_wings + 1):
        minimum_cost = float('inf')
        for i in range(1, j + 1): #loop over all possible split points
            if minimum_cost > price_of_orders[i].price + optimal_wing_prices[j - i]:
                minimum_cost = price_of_orders[i].price + optimal_wing_prices[j - i]
                optimal_order_split[j] = i #Check to see if the current combo of wings and their respective prices is lower than the current minimum, and if so, update it to that order
        optimal_wing_prices[j] = minimum_cost #Store the minimum cost in the current j index of optimal wing prices
 
    optimal_order_combo = []
    while num_wings > 0:
        optimal_order_combo.append(price_of_orders[optimal_order_split[num_wings]]) #add the current order combo at the current split point
        previous_order_wings = price_of_orders[optimal_order_split[num_wings]].wings
        num_wings -= previous_order_wings #decrease the number of wings by the amount that was in the wings of the last appended order

    return optimal_order_combo #return the optimal order combination for the wings

#  DO NOT EDIT BELOW THIS LINE

#Order class: represents a single valid order of chicken wings 
#Has two instance variables: the number of wings in the order size, and the price.
class Order:
    def __init__(self,wings,price):
        self.wings = wings
        self.price = price
    def __repr__(self):
        return str(self.wings) + " wings: $"+ str(self.price)
    def __eq__(self,other):
        return self.wings == other.wings and self.price == other.price

pL1 = [Order(1,4)]
pL2 = [Order(1,2), Order(5,5), Order(7,6)]
pL3 = [Order(1,2), Order(3,3), Order(4,6), Order(5,10),
       Order(6,11), Order(7,13), Order(8,14), Order(9,19)]
pL4 = [Order(1,1), Order(2,5), Order(3,8), Order(4,9),
       Order(5,12), Order(6,17), Order(7,19), Order(8,20)]
pL5 = [Order(1,4), Order(6,7), Order(8,9), Order(10,11),
       Order(12,16), Order(15,21), Order(24,24), Order(27,32),
       Order(30,34), Order(34,36), Order(37,39), Order(41,41),
       Order(48,49), Order(50,53)]
pL6 = [Order(4,4.55), Order(5,5.70), Order(6,6.80), Order(7,7.95),
       Order(8,9.10), Order(9,10.20), Order(10,11.35), Order(11,12.50),
       Order(13,14.75), Order(14,15.90), Order(15,17.00), Order(16,18.15),
       Order(17,19.30), Order(18,20.40), Order(19,21.55), Order(20,22.70),
       Order(21,23.80), Order(22,24.95), Order(23,26.10), Order(24,27.25),
       Order(25,27.80), Order(26,28.95), Order(27,30.10), Order(28,31.20),
       Order(29,32.35), Order(30,33.50), Order(35,39.15), Order(40,44.80),
       Order(45,50.50), Order(50,55.60), Order(60,67.00), Order(70,78.30),
       Order(75,83.45), Order(80,89.10), Order(90,100.45), Order(100,111.25),
       Order(125,139.00), Order(150,166.85), Order(200,222.50)]
       

price_lists = [ list(pL1),list(pL1),list(pL2),list(pL2),list(pL3),list(pL3),
                list(pL4),list(pL4),list(pL5),list(pL5),list(pL6),list(pL6)]
wing_nums = [ 1, 3, 10, 15, 4, 8, 3, 6, 35, 55, 19, 394]
correct = [[Order(1,4)],
           [Order(1,4), Order(1,4), Order(1,4)],
           [Order(5,5), Order(5,5)],
           [Order(7,6), Order(7,6), Order(1,2)],
           [Order(1,2), Order(3,3)],
           [Order(3,3), Order(3,3), Order(3,3)],
           [Order(1,1), Order(1,1), Order(1,1)],
           [Order(1,1), Order(1,1), Order(1,1), Order(1,1), Order(1,1), Order(1,1)],
           [Order(6,7), Order(6,7), Order(24,24)],
           [Order(6,7), Order(8,9), Order(41,41)],
           [Order(4,4.55), Order(6,6.80), Order(9,10.20)],
           [Order(25,27.80), Order(25,27.80), Order(25,27.80), Order(26,28.95),
            Order(28,31.20), Order(28,31.20), Order(28,31.20), Order(28,31.20),
            Order(28,31.20), Order(28,31.20), Order(125,139.00)]] 

def compute_cost(price_list, orders):
    total = 0
    for ele in orders:
        assert ele in price_list, "Invalid order "+str(ele)
        total += ele.price
    return total

#Run test cases
count = 0

try:
    for i in range(len(price_lists)):
        
        if i%2 == 0:
            print("\n---------------------------------------\n")
            print("Price List: ")
            for ele in price_lists[i]:
                print(ele)
            print("\n")
        print("TEST #",i+1)
        print("Wings needed:",wing_nums[i])
        out_orders = optimize_wings(price_lists[i],wing_nums[i])
        corr_orders = correct[i]
        corr_cost = round(compute_cost(price_lists[i],corr_orders),2)
        print("Optimal Order:",corr_orders," Cost $"+str(corr_cost))
        for ele in out_orders:
            assert type(ele) == Order, \
                   str(ele)+" in output list: "+str(out_orders)+\
                   "  is not an Order object"
        out_cost = round(compute_cost(price_lists[i],out_orders),2)
        print("Output Order:",out_orders," Cost $"+str(out_cost))
        assert sum(map(lambda x: x.wings,out_orders)) >= wing_nums[i], "Insufficient total wings ordered!"
        assert corr_cost == out_cost, "wings order not cheapest possible!"
        print("Test Passed!\n")
        count += 1
except AssertionError as e:
    print("\nFAIL: ",e)

except Exception:
    print("\nFAIL: ",traceback.format_exc())


print(count,"out of",len(price_lists),"tests passed.")

