import zmq
import time
import SystemVariables as sv
import socket
from threading import Thread

class Network():
    """ Generic class for pub-sub for home network

        Args:
            pubname (string): publisher name, connected to the systemvariables
            subscribtions (list of str): all strings that should be listened to
            timeout (float): timeout for listening socket

        Attributes:
            pubname (string): publisher name, connected to the systemvariables
            subs (list of str): all strings that should be listened to

    """
    def __init__(self,pubname = None,subscribtions = None,timeout = None):
        """ Initalize the listener

        """
        self._publisher = None
        self._subscriber = None
        self._poller = None
        self.pubname = pubname
        self.subs = subscribtions
        self.context = zmq.Context()
        self._timeout = timeout


    def createpublisher(self):
        """ Setup a publisher and bind

        """
        if self.pubname == None:
            raise NameError("publisher needs a proper name to start publishing")
        # create publisher
        
        address = 'tcp://' + sv.nodes[self.pubname][0] + ':' + str(sv.nodes[self.pubname][1])
        tries = 0
        while tries < 100:
            try: 
                publisher = self.context.socket(zmq.PUB)
                publisher.bind(address)
                tries = 100
            except zmq.error.ZMQError:
                # print('failed, connecting.... waiting and trying again')
                time.sleep(0.1)
                tries +=1 
        print('publishing to: ' + address)
        return publisher

    def setup_publisher(self):
        """ creates a publisher and makes is available for the object

        """
        
        self._publisher = self.createpublisher()
        self._publisher.setsockopt(zmq.HEARTBEAT_IVL,1000)
        

    def setuplistner(self,constant = False):
        """ Setup a listener with the init values given

        """
        # create subscriber
        self._subscriber = self.context.socket(zmq.SUB)

        # add all available nodes
        for node in sv.nodes.keys():
            address = 'tcp://' + sv.nodes[node][0] + ':' + str(sv.nodes[node][1])
            print('Subscribing to: ' + address)
            self._subscriber.connect(address)

        # handle if no subsciptions were given
        if self.subs == None:
            self._subscriber.setsockopt(zmq.SUBSCRIBE, ''.encode())
            print('Will listen to all messages, since no filter was provided.')

        # add filters
        for s in self.subs:
            print("filtering on: " + s)
            self._subscriber.setsockopt(zmq.SUBSCRIBE, s.encode())

        self._poller = zmq.Poller()
        self._poller.register(self._subscriber,zmq.POLLIN)

    def reset(self):
        """ resets the sockets

        """
        if self._subscriber:
            self._poller.unregister(self._subscriber)
            self._subscriber.close()
            self.setuplistner()

        if self._publisher:
            self._publisher.close()
            self.setup_publisher()

    def listen(self):
        """ listen for new publish with correct key word

            Returns a message string 
        """
        retstr = ''
        poll = self._poller.poll(self._timeout)
        if poll:
            retstr = poll[0][0].recv(zmq.DONTWAIT).decode()
        return retstr

    # def send(self,message):
    #     """ Publishes a message to the network

    #         Args:
    #             message (str): message to be sent

    #     """
    #     self._publisher.send(message.encode())
    def thread_send(self,message):
        if self._publisher == None:
            # print('new thread')
            publisher = self.createpublisher()
            time.sleep(1)
            publisher.send(message.encode())
            publisher.close()
            
        else:

            self._publisher.send(message.encode())

    def send(self,message):
        """ Publishes a message to the network

            Args:
                message (str): message to be sent

        """
        Thread(target=self.thread_send,args=(message,)).start()
