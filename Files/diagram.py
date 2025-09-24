import graphviz

flow = graphviz.Digraph(format='png')
flow.attr(rankdir='TB', size='12')

# Nodes
flow.node('Start', 'Start', shape='ellipse')
flow.node('Login', 'Login Page', shape='box')
flow.node('Signup', 'Signup Page', shape='box')
flow.node('Home', 'Home Page', shape='box')
flow.node('Food', 'Food Page', shape='box')
flow.node('Search', 'Search / Filter Items', shape='box')
flow.node('Cart', 'Add to Cart', shape='box')
flow.node('PlaceOrder', 'Place Order', shape='box')
flow.node('TrackOrder', 'Track Order', shape='box')
flow.node('About', 'About Page', shape='box')
flow.node('Logout', 'Logout', shape='box')
flow.node('Help', 'Help Page', shape='box')
flow.node('QR', 'Show QR Code', shape='box')
flow.node('OrderComplete', 'Order Completed', shape='box')
flow.node('Feedback', 'Feedback', shape='box')
flow.node('Exit', 'Exit', shape='ellipse')

# Edges
flow.edge('Start', 'Login')
flow.edge('Login', 'Signup', label='New user?')
flow.edge('Signup', 'Login', label='Signup success')
flow.edge('Login', 'Home', label='Login success')

# Home page options
flow.edge('Home', 'Food')
flow.edge('Home', 'About')
flow.edge('Home', 'Help')
flow.edge('Home', 'QR')
flow.edge('Home', 'Logout')

# Food page actions
flow.edge('Food', 'Search')
flow.edge('Search', 'Cart')
flow.edge('Cart', 'PlaceOrder')
flow.edge('PlaceOrder', 'OrderComplete')
flow.edge('OrderComplete', 'Food', label='Back to explore more item')
flow.edge('OrderComplete', 'TrackOrder')
flow.edge('TrackOrder', 'Feedback')
flow.edge('Feedback', 'Exit')

# Render flowchart
flow.render('khana_khazana_flowchart_final', format='png', cleanup=True)

# import graphviz

# dot = graphviz.Digraph(format='png')
# dot.attr(rankdir='LR', size='10')

# # Define nodes
# dot.node('User', 'User\n(Django built-in)', shape='box')
# dot.node('Profile', '''Profile
# ------------------------
# - name: CharField
# - email: EmailField
# - password: CharField
# - city: CharField
# - user: OneToOne (User)''', shape='box')

# dot.node('Item', '''Item
# ------------------------
# - name: CharField
# - description: TextField
# - price: DecimalField
# - image: ImageField (optional)
# - category: CharField (choices)''', shape='box')

# dot.node('Cart', '''Cart
# ------------------------
# - user: ForeignKey(Profile)
# - item: ForeignKey(Item)
# - quantity: PositiveIntegerField
# - get_total_price()''', shape='box')

# dot.node('Order', '''Order
# ------------------------
# - user: ForeignKey(Profile)
# - customer_name: CharField
# - address: TextField
# - phone: CharField
# - items: TextField
# - total: DecimalField
# - status: CharField
# - created_at: DateTimeField''', shape='box')

# # Define edges (relationships)
# dot.edge('Profile', 'User', label='OneToOne')
# dot.edge('Cart', 'Profile', label='ForeignKey')
# dot.edge('Cart', 'Item', label='ForeignKey')
# dot.edge('Order', 'Profile', label='ForeignKey')

# # Render the diagram to a file
# dot.render('django_model_relationships', format='png', cleanup=True)
