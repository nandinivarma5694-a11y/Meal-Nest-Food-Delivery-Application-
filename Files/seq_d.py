import graphviz

seq = graphviz.Digraph('SequenceDiagram', format='png')

# Graph settings
seq.attr(rankdir='LR', size='10')

# Define actors and components
seq.node('U', 'User', shape='box', style='filled', fillcolor='#ffcccc')
seq.node('L', 'Login View', shape='box', style='filled', fillcolor='#ccffcc')
seq.node('P', 'Profile Model', shape='box', style='filled', fillcolor='#ccccff')
seq.node('H', 'Home Page', shape='box', style='filled', fillcolor='#ffe0b2')
seq.node('F', 'Food View', shape='box', style='filled', fillcolor='#ccffcc')
seq.node('I', 'Item Model', shape='box', style='filled', fillcolor='#ccccff')
seq.node('C', 'Cart View', shape='box', style='filled', fillcolor='#ccffcc')
seq.node('CM', 'Cart Model', shape='box', style='filled', fillcolor='#ccccff')
seq.node('D', 'Customer Details View', shape='box', style='filled', fillcolor='#ccffcc')
seq.node('O', 'Order Summary View', shape='box', style='filled', fillcolor='#ccffcc')
seq.node('OM', 'Order Model', shape='box', style='filled', fillcolor='#ccccff')
seq.node('T', 'Track Orders View', shape='box', style='filled', fillcolor='#ccffcc')

# Sequence flow
# Login
seq.edge('U', 'L', 'Enter Email & Password')
seq.edge('L', 'P', 'Check User in DB')
seq.edge('P', 'L', 'Return User Data')
seq.edge('L', 'U', 'Login Success / Error')
seq.edge('L', 'H', 'Redirect to Home')

# Food ordering
seq.edge('U', 'F', 'Browse Food Menu')
seq.edge('F', 'I', 'Fetch Items')
seq.edge('I', 'F', 'Return Items')
seq.edge('F', 'U', 'Display Food List')
seq.edge('U', 'C', 'Add Item to Cart')
seq.edge('C', 'CM', 'Save Item in Cart')
seq.edge('CM', 'C', 'Confirm Cart Save')
seq.edge('C', 'U', 'Item Added Message')

# Checkout & Order
seq.edge('U', 'D', 'Enter Customer Details')
seq.edge('D', 'O', 'Send Data to Order')
seq.edge('O', 'OM', 'Create Order')
seq.edge('OM', 'O', 'Order ID')
seq.edge('O', 'U', 'Order Placed Message')

# Track Orders
seq.edge('U', 'T', 'Request Order History')
seq.edge('T', 'OM', 'Fetch Orders')
seq.edge('OM', 'T', 'Return Orders')
seq.edge('T', 'U', 'Show Order History')

# Save diagram
seq.render('mealnest_sequence')
