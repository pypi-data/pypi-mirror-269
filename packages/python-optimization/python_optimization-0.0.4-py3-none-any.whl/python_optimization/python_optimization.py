def set():
    '''
    import numpy as np

    def union(A, B):
        result = {}
        for i in A:
            if A[i] > B[i]:
                result[i] = A[i]
            else:
                result[i] = B[i]
        print("Union of two sets is", result, '\n')


    def intersection(A, B):
        result = {}
        for i in A:
            if A[i] < B[i]:
                result[i] = A[i]
            else:
                result[i] = B[i]
        print("Intersection of two sets is", result, '\n')


    def complement(A, B):
        result = {}
        result1 = {}
        for i in A:
            result[i] = round(1 - A[i], 2)
        for i in B:
            result1[i] = round(1 - B[i], 2)
        print("Complement of  1st set is", result)
        print("Complement of  2nd set is", result1, '\n')


    def difference(A, B):
        result = {}
        for i in A:
            result[i] = round(min(A[i], 1 - B[i]), 2)
        print("Difference of two sets is", result, '\n')


    def cartprod(A, B):
        R = [[] for i in range(len(A))]
        i = 0
        for x in A:
            for y in B:
                R[i].append(min(A[x], B[y]))
            i += 1
        print("Cartesian Product is", R, "\n")


    def maxmin():
        R = [[0.5, 0.8, 0.2], [0.3, 0.6, 0.4]]
        S = [[0.7, 0.4], [0.5, 0.6], [0.2, 0.8]]

        print("\nR:", R)
        print("S:", S)

        m, n = len(R), len(R[0])
        o = len(S[0])
        composition = np.zeros((m, o))

        for i in range(m):
            for k in range(o):
                composition[i][k] = max([min(R[i][j], S[j][k]) for j in range(n)])

        return composition


    A = {'a': 0.5, 'b': 0.8, 'c': 0.2}
    B = {'a': 0.7, 'b': 0.4, 'c': 0.6}

    print(A)
    print(B)
    print('\n')

    union(A, B)
    intersection(A, B)
    complement(A, B)
    difference(A, B)
    cartprod(A, B)

    result = maxmin()
    print("Max-Min Composition is", result)
    '''
    return 0

def milk():
    '''
    import random
    from deap import base, creator, tools, algorithms
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.datasets import load_iris
    from sklearn.preprocessing import StandardScaler


    iris = load_iris()
    X = iris.data
    y = iris.target

    scaler = StandardScaler()
    X_normalized = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

    def evaluate(individual):
        neurons = individual[0]
        layers = individual[1]

        model = MLPClassifier(hidden_layer_sizes=(neurons,) * layers, random_state=42, max_iter=10000)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f'n_Neurons: {neurons}. n_Layers:{layers}. ___ACC___: {accuracy}\n')

        return accuracy,

    POPULATION_SIZE = 10
    GENERATIONS = 5

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    toolbox.register("attr_neurons", random.randint, 1, 100)
    toolbox.register("attr_layers", random.randint, 1, 5)
    toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_neurons, toolbox.attr_layers), n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=1, up=100, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=POPULATION_SIZE)

    for gen in range(GENERATIONS):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

        fitnesses = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=len(population))

    best_individual = tools.selBest(population, k=1)[0]
    best_params = best_individual

    print("Best Parameters:", best_params)
    '''
    return 0


def art():
    '''
    import tensorflow_hub as hub
    import tensorflow as tf
    from matplotlib import pyplot as plt
    import numpy as np
    import cv2

    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')


    def load_image(img_path):
        img = tf.io.read_file(img_path)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = img[tf.newaxis, :]
        return img

    content_image = load_image('car1.jpeg')
    style_image = load_image('tree.jpg')

    stylized_image = model(tf.constant(load_image('car1.jpeg')), tf.constant(load_image('tree.jpg')))[0]

    plt.imshow(np.squeeze(stylized_image))
    plt.show()

    '''
    return 0

def deap():
    '''
    import random
    import numpy as np
    from deap import base, creator, tools, algorithms
    
    # Create the FitnessMax and Individual classes using the creator
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Define the evaluation function
    def evalOneMax(individual):
        return sum(individual),

    toolbox.register("evaluate", evalOneMax)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    def main():
        pop = toolbox.population(n=300)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
                                    stats=stats, halloffame=hof, verbose=True)

    main()
    '''
    return 0

def ant():
    '''
    import numpy as np
    from numpy import inf

    d = np.array([[0,10,12,11,14],[10,0,13,15,8],[12,13,0,9,14],[11,15,9,0,16],[14,8,14,16,0]])

    iteration = 100
    n_ants = 5
    n_citys = 5
    m = n_ants
    n = n_citys
    e = .5        
    alpha = 1    
    beta = 2      
    visibility = 1/d
    visibility[visibility == inf ] = 0

    pheromne = .1*np.ones((m,n))


    rute = np.ones((m,n+1))

    for ite in range(iteration):

        rute[:,0] = 1          

        for i in range(m):

            temp_visibility = np.array(visibility)        
            for j in range(n-1):
                #print(rute)

                combine_feature = np.zeros(5)     
                cum_prob = np.zeros(5)            

                cur_loc = int(rute[i,j]-1)       

                temp_visibility[:,cur_loc] = 0     

                p_feature = np.power(pheromne[cur_loc,:],beta)        
                v_feature = np.power(temp_visibility[cur_loc,:],alpha)  

                p_feature = p_feature[:,np.newaxis]                    
                v_feature = v_feature[:,np.newaxis]                     

                combine_feature = np.multiply(p_feature,v_feature)     

                total = np.sum(combine_feature)                       

                probs = combine_feature/total   
                cum_prob = np.cumsum(probs)     
                r = np.random.random_sample()  
                city = np.nonzero(cum_prob>r)[0][0]+1       

                rute[i,j+1] = city              

            left = list(set([i for i in range(1,n+1)])-set(rute[i,:-2]))[0]    

            rute[i,-2] = left                   
        rute_opt = np.array(rute)              

        dist_cost = np.zeros((m,1))             

        for i in range(m):

            s = 0
            for j in range(n-1):

                s = s + d[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1]  
            dist_cost[i]=s                      

        dist_min_loc = np.argmin(dist_cost)             
        dist_min_cost = dist_cost[dist_min_loc]         

        best_route = rute[dist_min_loc,:]               
        pheromne = (1-e)*pheromne                       

        for i in range(m):
            for j in range(n-1):
                dt = 1/dist_cost[i]
                pheromne[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1] = pheromne[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1] + dt

    print('route of all the ants at the end :')
    print(rute_opt)
    print()
    print('best path :',best_route)
    print('cost of the best path',int(dist_min_cost[0]) + d[int(best_route[-2])-1,0])
    '''
    return 0


def rpcc():
    '''
    import xmlrpc.client

    with xmlrpc.client.ServerProxy("http://127.0.0.1:8000/") as proxy:
        print('Connection Established')
        u_i = input('Enter no.: ')

        try:
            if not u_i:
                raise ValueError("No input provided")

            num = int(u_i)

            result = proxy.factorial(num)
            print(f"Factorial of {num}: {result}")

        except ValueError as ve:
            print(f"Error: {ve}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    '''
    return 0

def rpcs():
    '''
    from xmlrpc.server import SimpleXMLRPCServer
    import math

    def factorial(n: int):
        return math.factorial(n)

    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(factorial, "factorial")
    server.serve_forever()

    '''
    return 0

def rmic():
    '''
    import Pyro5.api

    def main():
        uri = "PYRONAME:string_concatenation_server"
        with Pyro5.api.Proxy(uri) as server:
            str1 = input("Enter the first string: ")
            str2 = input("Enter the second string: ")

            result = server.concatenate_strings(str1, str2)
            print(f"Concatenation result: {result}")


    if __name__ == "__main__":
        main()

    '''
    return 0

def rmis():
    '''
    import Pyro5.api
    @Pyro5.api.expose
    class StringConcatenationServer:
        def concatenate_strings(self, str1, str2):
            result = str1 + str2
            return result


    def main():
        daemon = Pyro5.api.Daemon()
        ns = Pyro5.api.locate_ns()

        uri = daemon.register(StringConcatenationServer)
        ns.register("string_concatenation_server", uri)

        print("Server is ready.")
        daemon.requestLoop()


    if __name__ == "__main__":
        main()

    '''
    return 0

def dload():
    '''
    import time
    import random


    class DynamicLoadBalancer:
        def __init__(self, servers):
            self.servers = {server: 0 for server in servers}

        def distribute_request(self, request):
            min_load_server = min(self.servers, key=self.servers.get)
            print(f"Request {request} sent to Server {min_load_server}")
            time.sleep(0.5)
            self.servers[min_load_server] += 1

        def display_server_loads(self):
            print("Current server loads:")
            for server, load in self.servers.items():
                print(f"Server {server}: {load}")


    def simulate_dynamic_load_balancing(load_balancer, num_requests):
        for i in range(1, num_requests + 1):
            load_balancer.distribute_request(i)
            if i % 5 == 0:
                load_balancer.display_server_loads()


    if __name__ == "__main__":
        server_addresses = ['Server B', 'Server A', 'Server C']
        dynamic_load_balancer = DynamicLoadBalancer(server_addresses)

        simulate_dynamic_load_balancing(dynamic_load_balancer, 20)

    '''
    return 0


def rload():
    '''
    import time

    class LoadBalancer:
        def __init__(self, servers):
            self.servers = servers
            self.current_server = 0

        def distribute_request(self, request):
            server = self.get_next_server()
            print(f"Request {request} sent to Server {server}")
            time.sleep(0.5)

        def get_next_server(self):
            next_server = self.current_server
            self.current_server = (self.current_server + 1) % len(self.servers)
            return self.servers[next_server]


    def simulate_client_requests(load_balancer, num_requests):
        for i in range(1, num_requests + 1):
            load_balancer.distribute_request(i)


    if __name__ == "__main__":
        server_addresses = ['Server A', 'Server B', 'Server C']
        load_balancer = LoadBalancer(server_addresses)

        simulate_client_requests(load_balancer, 10)

    '''
    return 0

def map():
    '''
    from mrjob.job import MRJob
    from mrjob.step import MRStep
    import csv
    from datetime import datetime


    class CalculateGrades(MRJob):

        def steps(self):
            return [
                MRStep(mapper=self.mapper,
                    reducer=self.reducer)
            ]

        def mapper(self, _, line):
            if line.startswith('date'):
                return
            
            temp = {}

            reader = csv.reader([line])
            for row in reader:
                date, tmx, tmn = str(row[0]), float(row[2]), float(row[3])
                temp[date] = tmx
            yield _, temp

        def reducer(self, key, value):
        t = list(value)
        for fun in [max, min]:
            max_pair = fun(t, key=lambda x: list(x.values())[0])
            
            max_pair_key = list(max_pair.keys())[0]
            max_pair_value = max_pair[max_pair_key]
            yield max_pair_key, max_pair_value


    if __name__ == "__main__":
        CalculateGrades.run()

    '''
    return 0

cjava = '''
        import java.rmi.Naming;
        import java.rmi.RemoteException;
        import java.util.InputMismatchException;
        import java.util.Map;
        import java.util.Scanner;

        public class HotelClient {
            public static void main(String[] args) {
                try (Scanner scanner = new Scanner(System.in)) {
                    HotelInterface hotelService = (HotelInterface) Naming.lookup("rmi://localhost:1099/HotelService");

                    while (true) {
                        System.out.println("1. Book a room");
                        System.out.println("2. Cancel booking");
                        System.out.println("3. View booked rooms");
                        System.out.println("4. Exit");
                        System.out.print("Enter your choice: ");

                        try {
                            int choice = scanner.nextInt();
                            scanner.nextLine();

                            switch (choice) {
                                case 1:
                                    System.out.print("Enter guest name: ");
                                    String guestName = scanner.nextLine();
                                    System.out.print("Enter room number: ");
                                    int roomNumber = scanner.nextInt();
                                    boolean booked = hotelService.bookRoom(guestName, roomNumber);
                                    if (booked) {
                                        System.out.println("Room booked successfully.");
                                    } else {
                                        System.out.println("Booking failed. Guest may already have a booking.");
                                    }
                                    break;
                                case 2:
                                    System.out.print("Enter guest name to cancel booking: ");
                                    String guestToCancel = scanner.nextLine();
                                    boolean canceled = hotelService.cancelBooking(guestToCancel);
                                    if (canceled) {
                                        System.out.println("Booking canceled successfully.");
                                    } else {
                                        System.out.println("Cancel booking failed. Guest may not have a booking.");
                                    }
                                    break;
                                case 3:
                                    displayBookedRooms(hotelService);
                                    break;
                                case 4:
                                    System.out.println("Exiting...");
                                    System.exit(0);
                                    break;
                                default:
                                    System.out.println("Invalid choice. Please enter a valid option.");
                            }
                        } catch (InputMismatchException e) {
                            System.out.println("Invalid input. Please enter a valid number.");
                            scanner.nextLine();
                        } catch (RemoteException e) {
                            System.out.println("RemoteException: " + e.getMessage());
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }

            private static void displayBookedRooms(HotelInterface hotelService) throws RemoteException {
                Map<String, Integer> bookings = hotelService.getBookings();
                if (bookings.isEmpty()) {
                    System.out.println("No rooms booked yet.");
                } else {
                    System.out.println("Booked Rooms:");
                    for (Map.Entry<String, Integer> entry : bookings.entrySet()) {
                        System.out.println("Room " + entry.getValue() + " - " + entry.getKey());
                    }
                }
            }
        }
        '''

sjava = '''
        import java.rmi.RemoteException;
        import java.rmi.server.UnicastRemoteObject;
        import java.util.HashMap;
        import java.util.Map;
        import java.util.concurrent.locks.Lock;
        import java.util.concurrent.locks.ReentrantLock;

        public class HotelServer extends UnicastRemoteObject implements HotelInterface {
        private Map<String, Integer> bookings;
        private Lock lock;

        public HotelServer() throws RemoteException {
            bookings = new HashMap<>();
            lock = new ReentrantLock();
        }

        @Override
        public boolean bookRoom(String guestName, int roomNumber) throws RemoteException {
            try {
            lock.lock();

            if (!bookings.containsKey(guestName)) {
                if (!bookings.containsValue(roomNumber)) {
                bookings.put(guestName, roomNumber);
                System.out.println("Booking successful for " + guestName + " in room " + roomNumber);
                return true;
                } else {
                System.out.println("Room " + roomNumber + " is already booked by someone else.");
                }
            } else {
                System.out.println(guestName + " already has a booking.");
            }

            return false;
            } finally {
            lock.unlock();
            }
        }

        @Override
        public synchronized boolean cancelBooking(String guestName) throws RemoteException {
            if (bookings.containsKey(guestName)) {
            int roomNumber = bookings.remove(guestName);
            System.out.println("Booking canceled for " + guestName + " in room " + roomNumber);
            return true;
            } else {
            System.out.println(guestName + " does not have a booking.");
            return false;
            }
        }

        @Override
        public synchronized Map<String, Integer> getBookings() throws RemoteException {
            return new HashMap<>(bookings);
        }

        public static void main(String[] args) {
            try {
            HotelServer server = new HotelServer();
            java.rmi.registry.LocateRegistry.createRegistry(1099);
            java.rmi.Naming.rebind("HotelService", server);
            System.out.println("HotelServer is ready.");
            } catch (Exception e) {
            e.printStackTrace();
            }
        }
        }
        '''