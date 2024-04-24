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
    return "Package not Installed properly"

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
    return "Package not Installed properly"


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
    return "Package not Installed properly"

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
    return "Package not Installed properly"

def ant():
    '''
import numpy as np
from numpy import inf

#given values for the problems

d = np.array([[0,10,12,11,14],[10,0,13,15,8],[12,13,0,9,14],[11,15,9,0,16],[14,8,14,16,0]])

iteration = 100
n_ants = 5
n_citys = 5

# intialization part
m = n_ants
n = n_citys
e = .5         #evaporation rate
alpha = 1     #pheromone factor
beta = 2       #visibility factor

#calculating the visibility of the next city visibility(i,j)=1/d(i,j)
visibility = 1/d
visibility[visibility == inf ] = 0

#intializing pheromne present at the paths to the cities
pheromne = .1*np.ones((m,n))

#intializing the rute of the ants with size rute(n_ants,n_citys+1)
#note adding 1 because we want to come back to the source city

rute = np.ones((m,n+1))

for ite in range(iteration):

    rute[:,0] = 1          #initial starting and ending positon of every ants '1' i.e city '1'

    for i in range(m):

        temp_visibility = np.array(visibility)         #creating a copy of visibility

        for j in range(n-1):
            #print(rute)

            combine_feature = np.zeros(5)     #intializing combine_feature array to zero
            cum_prob = np.zeros(5)            #intializing cummulative probability array to zeros

            cur_loc = int(rute[i,j]-1)        #current city of the ant

            temp_visibility[:,cur_loc] = 0     #making visibility of the current city as zero

            p_feature = np.power(pheromne[cur_loc,:],beta)         #calculating pheromne feature
            v_feature = np.power(temp_visibility[cur_loc,:],alpha)  #calculating visibility feature

            p_feature = p_feature[:,np.newaxis]                     #adding axis to make a size[5,1]
            v_feature = v_feature[:,np.newaxis]                     #adding axis to make a size[5,1]

            combine_feature = np.multiply(p_feature,v_feature)     #calculating the combine feature

            total = np.sum(combine_feature)                        #sum of all the feature

            probs = combine_feature/total   #finding probability of element probs(i) = comine_feature(i)/total

            cum_prob = np.cumsum(probs)     #calculating cummulative sum
            #print(cum_prob)
            r = np.random.random_sample()   #randon no in [0,1)
            #print(r)
            city = np.nonzero(cum_prob>r)[0][0]+1       #finding the next city having probability higher then random(r)
            #print(city)

            rute[i,j+1] = city              #adding city to route

        left = list(set([i for i in range(1,n+1)])-set(rute[i,:-2]))[0]     #finding the last untraversed city to route

        rute[i,-2] = left                   #adding untraversed city to route

    rute_opt = np.array(rute)               #intializing optimal route

    dist_cost = np.zeros((m,1))             #intializing total_distance_of_tour with zero

    for i in range(m):

        s = 0
        for j in range(n-1):

            s = s + d[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1]   #calcualting total tour distance

        dist_cost[i]=s                      #storing distance of tour for 'i'th ant at location 'i'

    dist_min_loc = np.argmin(dist_cost)             #finding location of minimum of dist_cost
    dist_min_cost = dist_cost[dist_min_loc]         #finging min of dist_cost

    best_route = rute[dist_min_loc,:]               #intializing current traversed as best route
    pheromne = (1-e)*pheromne                       #evaporation of pheromne with (1-e)

    for i in range(m):
        for j in range(n-1):
            dt = 1/dist_cost[i]
            pheromne[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1] = pheromne[int(rute_opt[i,j])-1,int(rute_opt[i,j+1])-1] + dt
            #updating the pheromne with delta_distance
            #delta_distance will be more with min_dist i.e adding more weight to that route  peromne

print('route of all the ants at the end :')
print(rute_opt)
print()
print('best path :',best_route)
print('cost of the best path',int(dist_min_cost[0]) + d[int(best_route[-2])-1,0])
    '''
    return "Package not Installed properly"


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
    return "Package not Installed properly"

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
    return "Package not Installed properly"

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
    return "Package not Installed properly"

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
    return "Package not Installed properly"

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
    return "Package not Installed properly"


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
    return "Package not Installed properly"

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
    return "Package not Installed properly"

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
        import java.rmi.Remote;
        import java.rmi.RemoteException;
        import java.util.Map;

        public interface HotelInterface extends Remote {
        boolean bookRoom(String guestName, int roomNumber) throws RemoteException;

        boolean cancelBooking(String guestName) throws RemoteException;

        Map<String, Integer> getBookings() throws RemoteException;
        }

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

def install():
    """
    deap==1.4.1
    sklearn==1.3.2
    tensorflow_hub==0.16.1
    tensorflow==2.16.1
    cv2==4.8.0.76
    matplotlib==3.8.0
    pyro5==5.15
    mrjob==0.7.4
    neattext==0.1.3"""
    return "Package not Installed properly"

def house():
    """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

%matplotlib inline

data = pd.read_csv('USA_Housing.csv')

data.head()

data.info()

data.isnull().sum()
scaler = StandardScaler()

X=data.drop(['Price','Address'],axis=1)
y=data['Price']

cols = X.columns

X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


lr = LinearRegression()
lr.fit(X_train,y_train)

pred = lr.predict(X_test)

r2_score(y_test,pred)
y_pred = lr.predict(X_test)

sns.scatterplot(x=y_test, y=pred)
sns.histplot((y_test-pred),bins=50,kde=True)

cdf=pd.DataFrame(lr.coef_, cols, ['coefficients']).sort_values('coefficients',ascending=False)
cdf"""
    return "Package not Installed properly"

def mclass():
    """import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Training data shape:", x_train.shape)
print("Training labels shape:", y_train.shape)
print("Test data shape:", x_test.shape)
print("Test labels shape:", y_test.shape)

print("Sample values in training data:")
print(x_train[0])

# Normalize pixel values to be between 0 and 1
x_train, x_test = x_train / 255.0, x_test / 255.0

# Add a channel dimension (for CNN input)
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

predictions = np.argmax(model.predict(x_test), axis=1)
true_labels = np.argmax(y_test, axis=1)

conf_matrix = confusion_matrix(true_labels, predictions)
print("Confusion Matrix:")
print(conf_matrix)

# Display an example confusion matrix plot
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
"""
    return "Package not Installed properly"

def rnn():
    """# EDA
import pandas as pd
import numpy as np

# Load Data Viz Pkgs
import seaborn as sns

# Load Text Cleaning Pkgs
import neattext.functions as nfx

# Load ML Pkgs
# Estimators
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

# Transformers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

# Load Dataset
df = pd.read_csv("emotion_dataset_raw.csv")

df.head()

# Data Cleaning
dir(nfx)

# User handles
df['Clean_Text'] = df['Text'].apply(nfx.remove_userhandles)

# Stopwords
df['Clean_Text'] = df['Clean_Text'].apply(nfx.remove_stopwords)

df.head()

# Features & Labels
Xfeatures = df['Clean_Text']
ylabels = df['Emotion']

#  Split Data
x_train,x_test,y_train,y_test = train_test_split(Xfeatures,ylabels,test_size=0.3,random_state=42)

# Build Pipeline
from sklearn.pipeline import Pipeline

# LogisticRegression Pipeline
pipe_lr = Pipeline(steps=[('cv',CountVectorizer()),('lr',LogisticRegression())])

# Train and Fit Data
pipe_lr.fit(x_train,y_train)

pipe_lr

# Check Accuracy
pipe_lr.score(x_test,y_test)

def sentiment_analysis(text):
    emotion = pipe_lr.predict([text])
    return emotion

text = "This book was so interesting it made me sad"

sentiment_analysis(text)

pipe_lr.predict_proba([text])

import pickle
with open('sen_pipeline.pkl', 'wb') as file:
    pickle.dump(pipe_lr, file)"""
    return "Package not Installed properly"

def brain():
    """from keras.models import load_model
import tensorflow as tf
import cv2
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
labels = ['glioma_tumor','meningioma_tumor','no_tumor','pituitary_tumor']

model = load_model('braintumor.h5')

def brain_tumor(img,):
    img = cv2.resize(img,(150,150))
    img_array = np.array(img)
    img_array = img_array.reshape(1,150,150,3)
    # img_array.shape
    with tf.device('/cpu:0'):
        a=model.predict(img_array, verbose=False)
    indices = a.argmax()
    return [labels[indices]]

if __name__ == '__main__':
#     img = image.load_img('input/testing/pituitary_tumor/image(15).jpg')
    img = cv2.imread('input/Testing/pituitary_tumor/image(15).jpg')
    plt.imshow(img)
    plt.show()
    print(brain_tumor(img))"""
    return "Package not Installed properly"

def dcgan():
    """import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, Dense, Flatten, Reshape, LeakyReLU
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt

# Hyperparameters
latent_dim = 100  # Dimension of random noise input
image_size = 28  # Size of MNIST images (28x28 pixels)
num_epochs = 5
batch_size = 128

def create_generator():
    model = tf.keras.Sequential()
    model.add(Dense(7 * 7 * 256, use_bias=False, input_shape=(latent_dim,)))
    model.add(Reshape((7, 7, 256)))
    model.add(Conv2DTranspose(128, (3, 3), strides=2, padding='same', activation='relu'))
    model.add(Conv2DTranspose(64, (3, 3), strides=2, padding='same', activation='relu'))
    model.add(Conv2DTranspose(1, (3, 3), activation='tanh', padding='same'))
    return model

def create_discriminator():
    model = tf.keras.Sequential()
    model.add(Conv2D(64, (3, 3), strides=2, padding='same', input_shape=(image_size, image_size, 1)))
    model.add(LeakyReLU(alpha=0.2))  
    model.add(Conv2D(128, (3, 3), strides=2, padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Conv2D(256, (3, 3), strides=2, padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    return model

def create_gan(generator, discriminator):
    discriminator.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0002, beta_1=0.5))
    discriminator.trainable = False  

    gan_input = tf.keras.Input(shape=(latent_dim,))
    generated_image = generator(gan_input)
    gan_output = discriminator(generated_image)

    gan_model = Model(inputs=gan_input, outputs=gan_output)
    gan_model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0002, beta_1=0.5))
    return gan_model

def train_gan(generator, discriminator, gan_model, dataset, epochs, batch_size, latent_dim):
    for epoch in range(epochs):
        for batch in range(dataset.shape[0] // batch_size):
            # Train discriminator
            noise = tf.random.normal(shape=(batch_size, latent_dim))
            fake_images = generator.predict(noise)
            real_images = dataset[np.random.randint(0, dataset.shape[0], batch_size)]

            combined_images = np.concatenate([real_images, fake_images])
            labels = np.concatenate([np.ones((batch_size, 1)), np.zeros((batch_size, 1))])
            labels += 0.05 * np.random.random(labels.shape)

            discriminator_loss = discriminator.train_on_batch(combined_images, labels)

            # Train generator
            noise = tf.random.normal(shape=(batch_size, latent_dim))
            misleading_targets = np.ones((batch_size, 1))

            generator_loss = gan_model.train_on_batch(noise, misleading_targets)

        print(f'Epoch {epoch + 1}, Discriminator Loss: {discriminator_loss}, Generator Loss: {generator_loss}')

def plot_generated_images(generator, latent_dim, examples=10, figsize=(10, 10)):
    noise = np.random.normal(0, 1, size=[examples, latent_dim])
    generated_images = generator.predict(noise)
    plt.figure(figsize=figsize)
    for i in range(examples):
        plt.subplot(1, examples, i+1)
        plt.imshow(generated_images[i, :, :, 0], cmap='gray')
        plt.axis('off')
    plt.tight_layout()
    plt.show()

# Load MNIST dataset
(train_images, _), (_, _) = mnist.load_data()
train_images = train_images.reshape(-1, image_size, image_size, 1)
train_images = train_images.astype('float32') / 255.0

# Create models
generator = create_generator()
discriminator = create_discriminator()
gan_model = create_gan(generator, discriminator)
print('created')
# Train GAN
train_gan(generator, discriminator, gan_model, train_images, num_epochs, batch_size, latent_dim)
print('tarined')
# Display generated images
plot_generated_images(generator, latent_dim)
"""
    return "Package not Installed properly"

def classify():
    """import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def analyze_review(text):
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(text)['compound']

        if sentiment_score >= 0.05:
            return ['positive']
        elif sentiment_score <= -0.05:
            return ['negative']
        else:
            return ['neutral']
    except Exception as e:
        return str(e)
if __name__ == "__main__":
    import os
    os.system('cls')
    text = str(input('ENTER REVIEW FOR CLASSIFICATION: '))
    sentiment = analyze_review(text)
    print(f"Sentiment: {sentiment}")
"""
    return "Package not Installed properly"

def btrain():
    """import keras
from keras.models import Sequential
from keras.layers import Conv2D,Flatten,Dense,MaxPooling2D,Dropout
from sklearn.metrics import accuracy_score

import ipywidgets as widgets
import io
from PIL import Image
import tqdm
from sklearn.model_selection import train_test_split
import cv2
from sklearn.utils import shuffle
import tensorflow as tf


X_train = []
Y_train = []
image_size = 150
labels = ['glioma_tumor','meningioma_tumor','no_tumor','pituitary_tumor']
for i in labels:
    folderPath = os.path.join('input/Training',i)
    for j in os.listdir(folderPath):
        img = cv2.imread(os.path.join(folderPath,j))
        img = cv2.resize(img,(image_size,image_size))
        X_train.append(img)
        Y_train.append(i)

for i in labels:
    folderPath = os.path.join('input/Testing',i)
    for j in os.listdir(folderPath):
        img = cv2.imread(os.path.join(folderPath,j))
        img = cv2.resize(img,(image_size,image_size))
        X_train.append(img)
        Y_train.append(i)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

X_train,Y_train = shuffle(X_train,Y_train,random_state=101)
X_train.shape


X_train,X_test,y_train,y_test = train_test_split(X_train,Y_train,test_size=0.1,random_state=101)

y_train_new = []
for i in y_train:
    y_train_new.append(labels.index(i))
y_train=y_train_new
y_train = tf.keras.utils.to_categorical(y_train)

y_test_new = []
for i in y_test:
    y_test_new.append(labels.index(i))
y_test=y_test_new
y_test = tf.keras.utils.to_categorical(y_test)


model = Sequential()
model.add(Conv2D(32,(3,3),activation = 'relu',input_shape=(150,150,3)))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(Dropout(0.3))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Conv2D(128,(3,3),activation='relu'))
model.add(Conv2D(256,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(512,activation = 'relu'))
model.add(Dense(512,activation = 'relu'))
model.add(Dropout(0.3))
model.add(Dense(4,activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])

history = model.fit(X_train,y_train,epochs=20,validation_split=0.1)
model.save('braintumor.h5')"""

    return "Package not Installed properly"