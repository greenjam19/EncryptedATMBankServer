from random import randint
from bitstring import BitArray
from Crypto.Util.number import getPrime

KEY_SIZE = 512

# gcd calculation using euclidean algorithm
def euclidean_gcd(a, b):
    if (a < b):
        a, b = b, a
    
    while (b != 0):
        a, b = b, a % b
    
    return a

# driver functions to get the gcd using extended euclidean algo
def ext_euclidean_gcd(a, b):
    if (a < b):
        a, b = b, a

    v1 = [1, 0]
    v2 = [0, 1]

    return true_ext_euclidean_gcd(a, b, v1, v2)

# Function returns the extended euclidean gcd and factors to get it
def true_ext_euclidean_gcd(a, b, v1, v2):
    while (b != 0):
        a, b, v1, v2 = b, a % b, v2, [v1[0] - (a // b) * v2[0], v1[1] - (a // b) * v2[1]]
 
    return (a, b, v1)

# Function to calculate the modular inverse
def modular_inverse(a, n):
    # reducing a
    a %= n

    # returning the value corresponding to be in the return vector
    return ext_euclidean_gcd(n, a)[2][1] % n

# Plaintexts and ciphertexts are strings
class RSA():
    def public(self, key, msg):
        msg = pow(msg, key[0], key[1])

        return msg

    def private(self, key, msg):
        msg = pow(msg, key[0], key[1] * key[2])

        return msg

    # Returns all the components of the rsa key
    # (p, q, n, e, d), returns are all integers
    def key_generation(self):
        # key generation
        p = getPrime(KEY_SIZE)
        q = getPrime(KEY_SIZE)

        # Calculating n and the totient function
        n = p * q
        phi_n = (p -1) * (q - 1)

        # Calculating e
        e = randint(2, phi_n -1)
        while (euclidean_gcd(e, phi_n) != 1):
            e = randint(2, phi_n -1)

        # Calculating d
        d = modular_inverse(e, phi_n)

        return ((e, n), (d, p, q))

# HELPER FUNCTIONS FOR CASTING
# Casting hex string to int
def h_to_i(hexa : str) -> int:
    return int(hexa, base=16)

# Casting int to hex string
def i_to_h(integer : int) -> str:
    return hex(integer)

# Helper function to cast form text to hex
def t_to_h(text : str) -> str:
    ret = "0x"

    for char in text:
        ret += hex(ord(char))[2:]

    if ret == "0x":
        return "0x0"

    return ret

# Casting string to an integer
def t_to_i(text: str) -> int:
    return int(t_to_h(text), base=16)

# Helper function to cast form hex to text
def h_to_t(hexa : str) -> str:
    return str(BitArray(hexa).bytes, 'utf-8')

# Casting from an integer to text
def i_to_t(integer : int) -> str:
    return h_to_t(hex(integer))

if __name__ == "__main__":
    # Key generation of rsa
    rsa = RSA()
    public, private = rsa.key_generation()

    client_public =  (9547027239486902716735750934755686408233239156795884474499612594673375981503812440772160510257536226931364101380413927175868015049480606969456797668498154221518810458701795090788302002297098528887911675107205692380830508969642062953795028556603418663020553084953781297980238782219073273202442721472774015961, 106708295143382034670684117277229306541407787271548816426597303416896988268369420589108598021324775665192026367501310026261869917056697425881536550549065710387857538233011146081661294114314836098923510575630802026173185349871951492275861341115018986603708389373478965801340713159155528975995847535436361371561)
    client_private =  (77611350717571083614767448309337556711976928793365469578567388002878628980953465086457401555376595050559707166192504863391389258603337013740114924433066039901747439513794001530099211182388644020511705746599459231369269305199408601036765445725276288226102302984734750128796339792184480285050065980817479638201, 12183299158408310295412919328069188598247871415734610571292105427748879069351843582895960983824204878933107105386909474568682974400388183295462510169324813, 8758571365272373607189611640933589375225283950041383680326956052158951231848694608338599836096117426355045468454391551328545797499974027941997595854441997)
    server_public =  (25972465746138436197202895911347415948588186717525030577532457750022538085952395223242457316938300726240816226390426092108976524446832000173890159870858391695057408857167398643586892498038694470953335725760720035150168744426134334524951081689923853054606699404609242638713524024603663645895647091378664149533, 103930535430459924315994452610307291119984989196724814501370855500700055974244363613288682165898456214059243081649625651593069522316991946018234304315992902197049456989070847902541432054746455141311860482494917798804512926894683307458249151973589680880113569354680945037166224186659985231627343378327673388161)
    server_private =  (94724705562502753746004239043290490632206843801078323402906827193558724393162269886712712027477721344119556394530941145692588277571587792583849798785277343172129788687362847475413694206929747357338412831357727446114317082098090734372861424643289413083752180109676038160785350607465895954811778013432109599797, 8732269358370239086102326204451550232255386927722699282035317098732980670669476631623739657264480015665852722625179918377461505416772898898036496632733681, 11901892986253136413371320706907076719191489316498713765437267705844342890200774204698947563807792965642816626114088220638846480713073685640345934793160081)

    # Round trip of encryption
    msg = "Client this is server"


    print("Sanity checks:")
    # Sanity check 1
    print(rsa.public(server_public, rsa.private(server_private, t_to_i(msg))) == t_to_i(msg))
    print(rsa.private(server_private, rsa.public(server_public, t_to_i(msg))) == t_to_i(msg))

    # Sanity check 2
    print(rsa.public(client_public, rsa.private(client_private, t_to_i(msg))) == t_to_i(msg))
    print(rsa.private(client_private, rsa.public(client_public, t_to_i(msg))) == t_to_i(msg))
    print()

    # Performing the actual round trip from the server side
    print("trip from server to client:")
    ciphertext = rsa.public(client_public, rsa.private(server_private, t_to_i(msg)))
    print(ciphertext)

    plaintext = rsa.public(server_public, rsa.private(client_private, ciphertext))
    print(i_to_t(plaintext) == msg)
    print()

    # Performing
    print("trip from client to server:")
    ciphertext = rsa.public(server_public, rsa.private(client_private, t_to_i(msg)))
    print(ciphertext)

    plaintext = rsa.public(client_public, rsa.private(server_private, ciphertext))
    print(i_to_t(plaintext) == msg)
    print()

