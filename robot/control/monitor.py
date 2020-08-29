from Communication import Network

sub = Network(subscribtions=[''])
sub.setuplistner()

while True:
    print(sub.listen())