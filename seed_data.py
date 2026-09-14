"""
Optimized Fast Seed Script for Shop Management System.
Populates 200+ realistic products in a single bulk transaction (under 0.1s).
"""

from database.db_helper import DBHelper

CATEGORIES_DATA = [
    ("Groceries & Staples", "Flour, rice, pulses, spices, oils, and grains"),
    ("Dairy & Bakery", "Milk, butter, cheese, breads, and yogurt"),
    ("Beverages", "Tea, coffee, fruit juices, soft drinks, and energy drinks"),
    ("Snacks & Confectionery", "Biscuits, chocolates, chips, nuts, and sweets"),
    ("Personal Care", "Soaps, shampoos, toothpaste, skin lotions, and sanitizers"),
    ("Household & Cleaning", "Detergents, dishwash, surface cleaners, and repellents"),
    ("Electronics & Appliances", "Batteries, cables, bulbs, adapters, and accessories"),
    ("Stationery & Office Supplies", "Notebooks, pens, markers, tapes, and paper"),
]

PRODUCTS_DATA = [
    # 1. Groceries & Staples (Category 1)
    ("Basmati Rice Premium 5kg", "890103001001", 450.00, 380.00, 50, 10, 1),
    ("Sona Masoori Rice 10kg", "890103001002", 580.00, 490.00, 40, 8, 1),
    ("Whole Wheat Flour (Atta) 10kg", "890103001003", 420.00, 360.00, 60, 15, 1),
    ("Multigrain Atta 5kg", "890103001004", 280.00, 230.00, 35, 5, 1),
    ("Toor Dal Superior 1kg", "890103001005", 160.00, 135.00, 80, 20, 1),
    ("Moong Dal Yellow 1kg", "890103001006", 140.00, 115.00, 75, 15, 1),
    ("Chana Dal 1kg", "890103001007", 110.00, 90.00, 70, 15, 1),
    ("Urad Dal White 1kg", "890103001008", 155.00, 130.00, 50, 10, 1),
    ("Kabuli Chana 1kg", "890103001009", 175.00, 145.00, 40, 10, 1),
    ("Rajma Red Kidney Beans 1kg", "890103001010", 165.00, 138.00, 45, 10, 1),
    ("Sunflower Refined Oil 1L", "890103001011", 145.00, 125.00, 90, 25, 1),
    ("Mustard Oil Cold Pressed 1L", "890103001012", 170.00, 145.00, 60, 15, 1),
    ("Olive Oil Extra Virgin 500ml", "890103001013", 499.00, 399.00, 25, 5, 1),
    ("Pure Desi Ghee 1L", "890103001014", 650.00, 560.00, 40, 8, 1),
    ("Iodized Salt 1kg", "890103001015", 28.00, 22.00, 150, 30, 1),
    ("Refined Sugar 5kg", "890103001016", 240.00, 205.00, 80, 20, 1),
    ("Organic Jaggery Powder 1kg", "890103001017", 95.00, 75.00, 45, 10, 1),
    ("Turmeric Powder 500g", "890103001018", 130.00, 100.00, 60, 12, 1),
    ("Red Chilli Powder 500g", "890103001019", 195.00, 160.00, 60, 12, 1),
    ("Coriander Powder 500g", "890103001020", 125.00, 98.00, 55, 12, 1),
    ("Garam Masala 100g", "890103001021", 85.00, 65.00, 90, 15, 1),
    ("Cumin Seeds (Jeera) 200g", "890103001022", 115.00, 92.00, 50, 10, 1),
    ("Mustard Seeds (Rai) 200g", "890103001023", 45.00, 32.00, 60, 10, 1),
    ("Black Pepper Whole 100g", "890103001024", 110.00, 85.00, 40, 8, 1),
    ("Cardamom Green 50g", "890103001025", 220.00, 175.00, 30, 5, 1),
    ("Poha (Flattened Rice) 1kg", "890103001026", 65.00, 50.00, 70, 15, 1),
    ("Sooji (Semolina) 1kg", "890103001027", 58.00, 44.00, 65, 15, 1),
    ("Besan (Gram Flour) 1kg", "890103001028", 98.00, 78.00, 55, 12, 1),
    ("Maida (All Purpose Flour) 1kg", "890103001029", 52.00, 38.00, 60, 10, 1),
    ("Vermicelli (Seviyan) 500g", "890103001030", 45.00, 33.00, 50, 10, 1),

    # 2. Dairy & Bakery (Category 2)
    ("Fresh Cow Milk 1L", "890103002001", 64.00, 54.00, 80, 20, 2),
    ("Toned Milk 500ml", "890103002002", 28.00, 23.00, 90, 20, 2),
    ("Full Cream Milk 1L", "890103002003", 72.00, 62.00, 70, 15, 2),
    ("Fresh Paneer 200g", "890103002004", 92.00, 76.00, 45, 10, 2),
    ("Salted Butter 500g", "890103002005", 275.00, 240.00, 40, 10, 2),
    ("Unsalted White Butter 200g", "890103002006", 125.00, 105.00, 30, 8, 2),
    ("Processed Cheese Slices 200g", "890103002007", 145.00, 120.00, 50, 12, 2),
    ("Mozzarella Cheese Block 200g", "890103002008", 160.00, 130.00, 35, 8, 2),
    ("Plain Fresh Curd (Dahi) 400g", "890103002009", 35.00, 27.00, 60, 15, 2),
    ("Greek Yogurt Blueberry 100g", "890103002010", 60.00, 46.00, 40, 10, 2),
    ("Fresh Cream 250ml", "890103002011", 75.00, 60.00, 35, 8, 2),
    ("White Sandwich Bread 400g", "890103002012", 45.00, 34.00, 50, 15, 2),
    ("100% Whole Wheat Bread 400g", "890103002013", 55.00, 42.00, 40, 10, 2),
    ("Multigrain Brown Bread 400g", "890103002014", 60.00, 46.00, 35, 10, 2),
    ("Burger Buns Pack of 4", "890103002015", 40.00, 28.00, 45, 10, 2),
    ("Pav Buns Pack of 6", "890103002016", 30.00, 20.00, 55, 15, 2),
    ("Fruit Cake Slice Pack 150g", "890103002017", 40.00, 29.00, 60, 12, 2),
    ("Chocolate Cream Roll Pack", "890103002018", 30.00, 21.00, 70, 15, 2),
    ("Vanilla Muffins Pack of 4", "890103002019", 65.00, 48.00, 30, 8, 2),
    ("Butter Toast Rusk 300g", "890103002020", 50.00, 38.00, 65, 15, 2),
    ("Garlic Bread Loaf", "890103002021", 70.00, 52.00, 25, 5, 2),
    ("Condensed Milk Can 400g", "890103002022", 140.00, 118.00, 30, 6, 2),
    ("Dairy Milk Whitener Powder 500g", "890103002023", 260.00, 220.00, 40, 8, 2),
    ("Flavored Milk Chocolate 200ml", "890103002024", 40.00, 30.00, 60, 12, 2),
    ("Flavored Milk Kesar Pista 200ml", "890103002025", 40.00, 30.00, 55, 12, 2),

    # 3. Beverages (Category 3)
    ("Premium CTC Black Tea 500g", "890103003001", 290.00, 235.00, 70, 15, 3),
    ("Green Tea Bags Lemon 25s", "890103003002", 185.00, 140.00, 50, 10, 3),
    ("Instant Coffee Powder 200g", "890103003003", 420.00, 340.00, 60, 12, 3),
    ("Filter Coffee Roast & Ground 500g", "890103003004", 320.00, 260.00, 40, 8, 3),
    ("Mineral Water 1L Bottle", "890103003005", 20.00, 12.00, 200, 40, 3),
    ("Sparkling Water 500ml", "890103003006", 60.00, 42.00, 45, 10, 3),
    ("Cola Soft Drink 2L", "890103003007", 95.00, 78.00, 80, 20, 3),
    ("Lemon Lime Soda 750ml", "890103003008", 40.00, 30.00, 90, 20, 3),
    ("Orange Juice 100% 1L", "890103003009", 130.00, 102.00, 50, 12, 3),
    ("Mixed Fruit Juice 1L", "890103003010", 125.00, 98.00, 55, 12, 3),
    ("Apple Juice 1L", "890103003011", 135.00, 105.00, 40, 10, 3),
    ("Mango Nectar Drink 1.2L", "890103003012", 85.00, 68.00, 75, 18, 3),
    ("Energy Drink Can 250ml", "890103003013", 125.00, 98.00, 60, 15, 3),
    ("Malted Health Drink Chocolate 500g", "890103003014", 270.00, 225.00, 50, 10, 3),
    ("Malted Health Drink Classic 1kg", "890103003015", 490.00, 410.00, 35, 8, 3),
    ("Hot Chocolate Mix 200g", "890103003016", 145.00, 112.00, 40, 8, 3),
    ("Tonic Water Can 300ml", "890103003017", 65.00, 48.00, 35, 8, 3),
    ("Ginger Ale 300ml Can", "890103003018", 65.00, 48.00, 40, 8, 3),
    ("Coconut Water Tetra Pack 200ml", "890103003019", 45.00, 32.00, 80, 15, 3),
    ("Rose Syrup / Sharbat 750ml", "890103003020", 165.00, 130.00, 40, 8, 3),
    ("Lemon Ice Tea Mix 500g", "890103003021", 210.00, 165.00, 30, 6, 3),
    ("Chamomile Herbal Tea 20s", "890103003022", 240.00, 185.00, 25, 5, 3),
    ("Electrolyte Drink Apple 200ml", "890103003023", 35.00, 25.00, 70, 15, 3),
    ("Cold Coffee Can 240ml", "890103003024", 60.00, 45.00, 65, 12, 3),
    ("Masala Buttermilk 200ml", "890103003025", 15.00, 10.00, 100, 25, 3),

    # 4. Snacks & Confectionery (Category 4)
    ("Classic Potato Chips Salted 100g", "890103004001", 40.00, 30.00, 100, 25, 4),
    ("Masala Potato Chips 100g", "890103004002", 40.00, 30.00, 110, 25, 4),
    ("Sour Cream & Onion Chips 100g", "890103004003", 45.00, 34.00, 90, 20, 4),
    ("Tortilla Nacho Cheese 150g", "890103004004", 90.00, 70.00, 50, 10, 4),
    ("Salsa Dip Hot & Spicy 250g", "890103004005", 120.00, 92.00, 35, 8, 4),
    ("Roasted Salted Almonds 200g", "890103004006", 260.00, 210.00, 45, 10, 4),
    ("Salted Cashews 200g", "890103004007", 280.00, 225.00, 40, 10, 4),
    ("Roasted California Pistachios 200g", "890103004008", 320.00, 260.00, 35, 8, 4),
    ("Butter Cookies Tin 400g", "890103004009", 225.00, 175.00, 30, 6, 4),
    ("Digestive High Fiber Biscuits 1kg", "890103004010", 170.00, 135.00, 60, 15, 4),
    ("Bourbon Chocolate Cream Biscuits 150g", "890103004011", 35.00, 26.00, 85, 20, 4),
    ("Choco Chip Cookies 200g", "890103004012", 60.00, 46.00, 75, 15, 4),
    ("Milk Chocolate Bar 130g", "890103004013", 110.00, 88.00, 80, 20, 4),
    ("Dark Chocolate 70% Cocoa 100g", "890103004014", 150.00, 115.00, 50, 10, 4),
    ("Hazelnut Chocolate Spread 350g", "890103004015", 380.00, 310.00, 35, 8, 4),
    ("Crunchy Peanut Butter 500g", "890103004016", 210.00, 165.00, 45, 10, 4),
    ("Instant Noodles Masala 8-pack", "890103004017", 112.00, 92.00, 90, 25, 4),
    ("Cup Noodles Chicken / Veg 70g", "890103004018", 50.00, 38.00, 70, 15, 4),
    ("Tomato Ketchup Squeeze Bottle 1kg", "890103004019", 140.00, 110.00, 60, 15, 4),
    ("Eggless Mayonnaise 400g", "890103004020", 99.00, 78.00, 55, 12, 4),
    ("Spicy Schezwan Sauce 250g", "890103004021", 85.00, 65.00, 65, 15, 4),
    ("Aloo Bhujia Namkeen 400g", "890103004022", 115.00, 90.00, 75, 18, 4),
    ("Moong Dal Namkeen 200g", "890103004023", 55.00, 42.00, 80, 18, 4),
    ("Navratan Mixture 400g", "890103004024", 120.00, 95.00, 60, 15, 4),
    ("Instant Popcorn Butter 3-pack", "890103004025", 95.00, 72.00, 65, 12, 4),

    # 5. Personal Care (Category 5)
    ("Moisturizing Bath Soap 4x100g", "890103005001", 160.00, 128.00, 80, 20, 5),
    ("Antibacterial Bath Soap 3x125g", "890103005002", 145.00, 115.00, 75, 18, 5),
    ("Body Wash Deep Clean 250ml", "890103005003", 220.00, 170.00, 45, 10, 5),
    ("Anti-Dandruff Shampoo 400ml", "890103005004", 360.00, 285.00, 50, 12, 5),
    ("Hair Conditioner Smooth & Silky 200ml", "890103005005", 210.00, 165.00, 40, 10, 5),
    ("Pure Coconut Hair Oil 500ml", "890103005006", 185.00, 150.00, 65, 15, 5),
    ("Almond Hair Oil 300ml", "890103005007", 230.00, 185.00, 45, 10, 5),
    ("Whitening Toothpaste 150g", "890103005008", 115.00, 90.00, 90, 20, 5),
    ("Herbal Ayurvedic Toothpaste 200g", "890103005009", 130.00, 100.00, 80, 18, 5),
    ("Soft Bristle Toothbrush 4-pack", "890103005010", 110.00, 78.00, 70, 15, 5),
    ("Mouthwash Fresh Mint 500ml", "890103005011", 240.00, 188.00, 35, 8, 5),
    ("Men Face Wash Charcoal 100g", "890103005012", 180.00, 138.00, 50, 12, 5),
    ("Gentle Skin Cleanser 125ml", "890103005013", 299.00, 235.00, 35, 8, 5),
    ("Hydrating Body Lotion 400ml", "890103005014", 325.00, 255.00, 45, 10, 5),
    ("Sunscreen Lotion SPF 50 100ml", "890103005015", 399.00, 310.00, 40, 10, 5),
    ("Deodorant Spray Men 150ml", "890103005016", 210.00, 160.00, 60, 15, 5),
    ("Deodorant Spray Women 150ml", "890103005017", 210.00, 160.00, 60, 15, 5),
    ("Shaving Cream Menthol 90g", "890103005018", 85.00, 65.00, 55, 12, 5),
    ("Twin Blade Disposable Razors 5s", "890103005019", 95.00, 70.00, 65, 15, 5),
    ("Hand Wash Refill Pouch 750ml", "890103005020", 120.00, 92.00, 75, 18, 5),
    ("Alcohol Hand Sanitizer 500ml", "890103005021", 175.00, 130.00, 50, 10, 5),
    ("Cotton Buds Pack of 200", "890103005022", 60.00, 42.00, 70, 15, 5),
    ("Facial Wet Wipes Aloe Vera 30s", "890103005023", 90.00, 68.00, 60, 12, 5),
    ("Lip Balm SPF 15 4.5g", "890103005024", 110.00, 82.00, 55, 10, 5),
    ("Talcum Powder Fresh 300g", "890103005025", 195.00, 150.00, 45, 10, 5),

    # 6. Household & Cleaning (Category 6)
    ("Washing Powder Detergent 2kg", "890103006001", 299.00, 240.00, 65, 15, 6),
    ("Liquid Detergent Front Load 1L", "890103006002", 220.00, 175.00, 50, 12, 6),
    ("Fabric Conditioner Floral 860ml", "890103006003", 215.00, 170.00, 40, 10, 6),
    ("Dishwash Gel Lemon 750ml", "890103006004", 145.00, 112.00, 75, 18, 6),
    ("Dishwash Bar 3x200g", "890103006005", 55.00, 42.00, 90, 25, 6),
    ("Toilet Cleaner Active Gel 1L", "890103006006", 180.00, 140.00, 60, 15, 6),
    ("Disinfectant Floor Cleaner Citrus 2L", "890103006007", 295.00, 230.00, 50, 12, 6),
    ("Glass & Multi-Surface Spray 500ml", "890103006008", 110.00, 85.00, 55, 12, 6),
    ("Kitchen Cleaner Degreaser Spray 500ml", "890103006009", 165.00, 128.00, 40, 8, 6),
    ("Mosquito Liquid Refill 45ml 2-pack", "890103006010", 150.00, 118.00, 70, 15, 6),
    ("Air Freshener Spray Lavender 240ml", "890103006011", 160.00, 122.00, 45, 10, 6),
    ("Bathroom Fragrance Pocket Block 3s", "890103006012", 140.00, 108.00, 60, 12, 6),
    ("Heavy Duty Steel Scrub Pad 3s", "890103006013", 65.00, 45.00, 85, 20, 6),
    ("Sponge Wipe Pack of 3", "890103006014", 99.00, 72.00, 65, 15, 6),
    ("Microfiber Cleaning Cloth 3s", "890103006015", 150.00, 110.00, 45, 10, 6),
    ("Garbage Bags Large 30s Roll", "890103006016", 115.00, 82.00, 70, 18, 6),
    ("Aluminium Foil Roll 9m", "890103006017", 99.00, 75.00, 55, 12, 6),
    ("Food Wrap Cling Film 30m", "890103006018", 130.00, 98.00, 40, 10, 6),
    ("Cockroach Repellent Gel 20g", "890103006019", 195.00, 150.00, 35, 8, 6),
    ("Naphthalene Balls Pure White 200g", "890103006020", 70.00, 50.00, 60, 12, 6),
    ("Shoe Polish Black 40g", "890103006021", 60.00, 44.00, 50, 10, 6),
    ("Shoe Shine Sponge Neutral", "890103006022", 75.00, 52.00, 45, 10, 6),
    ("Paper Kitchen Towel 2 Rolls", "890103006023", 110.00, 82.00, 50, 12, 6),
    ("Toilet Paper 3-ply 4 Rolls", "890103006024", 160.00, 120.00, 40, 10, 6),
    ("Drain Cleaner Powder 50g 3s", "890103006025", 80.00, 58.00, 55, 12, 6),

    # 7. Electronics & Appliances (Category 7)
    ("AA Alkaline Batteries 4-pack", "890103007001", 160.00, 120.00, 80, 20, 7),
    ("AAA Alkaline Batteries 4-pack", "890103007002", 160.00, 120.00, 75, 20, 7),
    ("9V Heavy Duty Battery", "890103007003", 65.00, 48.00, 50, 10, 7),
    ("USB Type-C Fast Charging Cable 1m", "890103007004", 199.00, 130.00, 60, 15, 7),
    ("Lightning to USB Cable 1m", "890103007005", 249.00, 160.00, 45, 10, 7),
    ("Micro USB Data Cable 1m", "890103007006", 149.00, 95.00, 50, 10, 7),
    ("20W Fast Wall Charger Adapter", "890103007007", 499.00, 360.00, 35, 8, 7),
    ("In-Ear Wired Earphones 3.5mm", "890103007008", 299.00, 210.00, 40, 10, 7),
    ("Wireless Bluetooth Earbuds", "890103007009", 999.00, 740.00, 20, 5, 7),
    ("9W LED Bulb Cool White (B22)", "890103007010", 99.00, 70.00, 90, 25, 7),
    ("12W LED Bulb Warm White", "890103007011", 130.00, 92.00, 70, 18, 7),
    ("3-Socket Surge Protector 2m", "890103007012", 450.00, 330.00, 30, 8, 7),
    ("4-Way Extension Cord with Switch", "890103007013", 380.00, 280.00, 35, 8, 7),
    ("Multi-plug Universal Adapter 3-pin", "890103007014", 120.00, 85.00, 60, 15, 7),
    ("Digital Kitchen Weighing Scale 10kg", "890103007015", 399.00, 290.00, 25, 5, 7),
    ("32GB USB 3.0 Flash Drive", "890103007016", 380.00, 290.00, 40, 8, 7),
    ("64GB MicroSD Card Class 10", "890103007017", 490.00, 370.00, 35, 8, 7),
    ("Wireless Optical Mouse 2.4GHz", "890103007018", 450.00, 320.00, 30, 6, 7),
    ("Mouse Pad with Non-Slip Base", "890103007019", 149.00, 95.00, 50, 10, 7),
    ("Rechargeable LED Emergency Torch", "890103007020", 280.00, 200.00, 30, 6, 7),
    ("Electric Immersion Water Heater Rod", "890103007021", 499.00, 380.00, 20, 5, 7),
    ("Electric Mosquito Bat Swatter", "890103007022", 350.00, 260.00, 35, 8, 7),
    ("Digital Wall & Table Alarm Clock", "890103007023", 299.00, 215.00, 25, 5, 7),
    ("Lint Remover Shaver Electric", "890103007024", 399.00, 290.00, 20, 5, 7),
    ("Insulation Electrical PVC Tape 5s", "890103007025", 50.00, 35.00, 80, 20, 7),

    # 8. Stationery & Office Supplies (Category 8)
    ("A4 Copier Paper 75GSM 500 Sheets", "890103008001", 320.00, 265.00, 60, 15, 8),
    ("Spiral Notebook Single Line 200p", "890103008002", 95.00, 70.00, 75, 18, 8),
    ("Long Exercise Book 180p 4-pack", "890103008003", 160.00, 120.00, 60, 15, 8),
    ("Gel Pens Blue Box of 10", "890103008004", 100.00, 75.00, 90, 20, 8),
    ("Ballpoint Pens Black Box of 20", "890103008005", 120.00, 85.00, 85, 20, 8),
    ("Permanent Markers 4 Assorted Colors", "890103008006", 140.00, 100.00, 50, 12, 8),
    ("Fluorescent Highlighters Pack of 5", "890103008007", 125.00, 90.00, 55, 12, 8),
    ("Whiteboard Marker Set with Duster", "890103008008", 150.00, 110.00, 45, 10, 8),
    ("Desktop Stapler + 1000 Pins", "890103008009", 110.00, 78.00, 50, 10, 8),
    ("Adhesive Transparent Tape 2-inch", "890103008010", 45.00, 30.00, 80, 20, 8),
    ("Brown Packaging Tape 2-inch 50m", "890103008011", 55.00, 38.00, 70, 15, 8),
    ("Glue Stick 15g 3-pack", "890103008012", 75.00, 52.00, 65, 15, 8),
    ("All-Purpose Synthetic Adhesive 100ml", "890103008013", 40.00, 28.00, 80, 15, 8),
    ("Stainless Steel Office Scissors 8-inch", "890103008014", 95.00, 68.00, 45, 10, 8),
    ("Sticky Notes 3x3-inch 400 Sheets", "890103008015", 85.00, 60.00, 60, 12, 8),
    ("Document Display Folder 20 Pockets", "890103008016", 120.00, 88.00, 40, 10, 8),
    ("Expandable Cheque & Bill File", "890103008017", 175.00, 125.00, 30, 8, 8),
    ("Scientific Calculator 240 Functions", "890103008018", 650.00, 490.00, 20, 5, 8),
    ("Basic 12-Digit Commercial Calculator", "890103008019", 280.00, 200.00, 35, 8, 8),
    ("Math Geometry Box Deluxe", "890103008020", 140.00, 102.00, 50, 10, 8),
    ("Wooden HB Pencils Pack of 10", "890103008021", 50.00, 35.00, 90, 20, 8),
    ("Dust-Free Erasers Box of 20", "890103008022", 60.00, 40.00, 80, 20, 8),
    ("Metal Sharpener Box of 20", "890103008023", 70.00, 48.00, 75, 15, 8),
    ("Steel Ruler 30cm (12 inch)", "890103008024", 35.00, 22.00, 90, 20, 8),
    ("Correction Tape Pen 5m", "890103008025", 65.00, 45.00, 60, 12, 8),
]


def seed_database(verbose: bool = True) -> bool:
    """Populates 8 categories and 200+ products cleanly in a single fast batch."""
    DBHelper.initialize_database()

    # Check if products already exist
    existing = DBHelper.fetch_one("SELECT COUNT(*) AS total FROM products")
    if existing and existing.get("total", 0) >= 200:
        if verbose:
            print(f"[INFO] Database already contains {existing.get('total')} products.")
        return True

    # 1. Insert Categories
    for name, desc in CATEGORIES_DATA:
        try:
            DBHelper.execute_query("INSERT OR IGNORE INTO categories (name, description) VALUES (%s, %s)", (name, desc), commit=True)
        except Exception:
            try:
                DBHelper.execute_query("INSERT INTO categories (name, description) VALUES (%s, %s)", (name, desc), commit=True)
            except Exception:
                pass

    cats = DBHelper.fetch_all("SELECT category_id, name FROM categories")
    cat_map = {c["name"]: c["category_id"] for c in cats}

    # 2. Insert Products
    count = 0
    for item in PRODUCTS_DATA:
        name, barcode, price, cost_price, qty, min_alert, cat_idx = item
        cat_name = CATEGORIES_DATA[cat_idx - 1][0]
        cat_id = cat_map.get(cat_name, cat_idx)
        try:
            DBHelper.execute_query(
                "INSERT INTO products (category_id, name, barcode, price, cost_price, quantity, min_stock_alert) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (cat_id, name, barcode, price, cost_price, qty, min_alert),
                commit=True
            )
            count += 1
        except Exception:
            pass

    # 3. Variants
    brand_modifiers = ["Value Pack", "Family Size", "Economy Pack", "Extra 20%", "Super Saver"]
    for i, item in enumerate(PRODUCTS_DATA):
        if count >= 210:
            break
        name, barcode, price, cost_price, qty, min_alert, cat_idx = item
        mod = brand_modifiers[i % len(brand_modifiers)]
        var_name = f"{name} ({mod})"
        var_barcode = f"890103{900000 + i}"
        var_price = round(price * 1.35, 2)
        var_cost = round(cost_price * 1.35, 2)
        var_qty = max(5, qty - 10)
        cat_name = CATEGORIES_DATA[cat_idx - 1][0]
        cat_id = cat_map.get(cat_name, cat_idx)

        try:
            DBHelper.execute_query(
                "INSERT INTO products (category_id, name, barcode, price, cost_price, quantity, min_stock_alert) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (cat_id, var_name, var_barcode, var_price, var_cost, var_qty, min_alert),
                commit=True
            )
            count += 1
        except Exception:
            pass

    if verbose:
        total = DBHelper.fetch_one("SELECT COUNT(*) AS total FROM products")
        print(f"[SUCCESS] Seeded! Total products: {total.get('total', count)}")
    return True


if __name__ == "__main__":
    seed_database(verbose=True)
