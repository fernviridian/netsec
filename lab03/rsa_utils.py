# THIS WAS DESIGNED FOR A NETSEC COURSE
# IT IS NOT VERY FAST.
# IT IS NOT VERY GOOD.
# DO NOT ACTUALLY USE THIS. IF YOU DO THE NSA WILL FACTOR YOUR KEYS IN NANOSECONDS.
# YOU HAVE BEEN WARNED.
# BUT FOR THE BASICS OF RSA IT GIVES YOU A GOOD IDEA.

import random
# not cryptographically secure, but pycrypto was being a butt.
import fractions

# formatting from prob00
def bit_to_hex(bits):
  return "%x" % bits

# integer public key for problem 6
def gen_pub_key(generator, privkey, p):
  return pow(generator, privkey, p)

def encrypt(msg, n, e):
  # all input is assumed to be a decimal integer
  #m^e % n
  return pow(msg, e, n)

def decrypt(ciphertext, n, d):
  # returns decimal integer
  return pow(ciphertext, d, n)

def is_prime(num):
  # TODO make this more efficient
  if num == 2:
    return True
  if num % 2 == 0 and num > 2:
  # all evens above 2 are not prime
    return False
  # check from 3 to sqrt(num) for all odd numbers
  for i in range(3, int(num**0.5)+1, 2):
    if num % i == 0:
      # ineligible due to divisibility by another number
      return False
  # if it passed all of thoses tests, it is prime
  return True

# slow, but accurate
def gen_prime(min_num, bound):
  # generate a prime random number
  prime = False
  while not prime:
    # generate a new random number
    # that should give us a good range
    num = random.randint(min_num, int(min_num * bound))
    # check
    if(is_prime(num) == True):
      prime = True
  # we have a prime, return that
  return num

def verify_signature(message, signature, N, e):
  # raises the signature to the power of e (modulo n)
  # The server's public key consists of the modulus N=3110232614083941699686461 and the public exponent e=3.
  #
  # based on the public key given, we take in the message and figure out what the signed version would be
  # modulus N
  # public exponent e
  #
  #https://www.cs.columbia.edu/~smb/classes/s09/l04.pdf
  serv_signature = int(signature)
  our_message = pow(serv_signature, e, N)
  # signatures match
  if(message == our_message):
    return True
  else:
    return False

# find coprimes
def coprime(phi):
  e = random.randrange(1, phi)
  g = fractions.gcd(e, phi)
  while (g != 1):
    e = random.randrange(1, phi)
    g = fractions.gcd(e, phi)
  return e

def mult_inverse(e, phi):
  # dont remember where this came from.....but it seems to work.
  # euclid multiplicitive inverse
  # TODO
  d = 0
  x1 = 0
  x2 = 1
  y1 = 1
  tmp_phi = phi
  
  while e > 0:
      tmp1 = tmp_phi/e
      tmp2 = tmp_phi - tmp1 * e
      tmp_phi = e
      e = tmp2
      
      x = x2- tmp1* x1
      y = d - tmp1 * y1
      
      x2 = x1
      x1 = x
      d = y1
      y1 = y
  
  if tmp_phi == 1:
      return d + phi

def gen_pq(min_num, bound):
  # generate a p and q
  p = 0
  q = 0
  while(p == q):
    p = gen_prime(min_num, bound)
    q = gen_prime(min_num, bound)
  return (p,q)

def check_n(min_num, bound, keylength):
  # check that n is withing bounds
  lower = 2**(keylength-1)
  upper = 2**keylength
  good = False
  while not good:
    p,q = gen_pq(min_num, bound)
    N = p * q
    if(N >= lower and N <= upper):
      good = True
      break

  return (N,p,q)

def gen_rsa(keylength, bound):
  # initialize our variables
  p = 0
  q = 0
  N = 0
  e = 0
  d = 0
  phi = 0
  # hackyhacky because sometimes we make a bad "d"
  good = False
  while not good:
    # calculate the fun RSA stuff.
    #Note: BOTH p and q must be "large". Here, that means if the requested key length is n, then both p and q must be at least 2 to the power (n/2)-1.
    # check if right amount of bits
    # before we genereat the primes we want to specify the minimum number for the key length
    min_num = 2**((keylength/2)-1)
    #Note: N should be a "large" number of about n bits. Here, N must be between 2 to the power n-1 and 2 to the power n.
    N,p,q = check_n(min_num, bound, keylength)
    phi = (p-1)*(q-1)
    # we have our p and q
    #Exponents e and d for the private and public keys, respectively.
    #Your private exponent e must be relatively prime with phi(N) = (p-1)*(q-1), and e and d must satisfy the equation e * d mod phi(N) == 1.
    # e, d prime
    # public exponent
    e = coprime(phi)
    # nice we have a valid e private key now
    # now we need to find the public key using extended euclidian algorithm
    # verifiy are euclidian primes
    # private exponent
    d = mult_inverse(e, phi)
    if d <= phi:
      good = True

  # a GOOD RSA KEYPAIR

  # DONE! now we need to construct the dictionary
  returned = {}
  returned['p'] = p
  returned['q'] = q
  returned['N'] = N
  returned['e'] = e
  returned['d'] = d
  returned['phi'] = phi
  return returned


def pretty_print(rsa_dict):
  # pretty print 
  p = rsa_dict['p']
  q = rsa_dict['q']
  N = rsa_dict['N']
  e = rsa_dict['e']
  d = rsa_dict['d']

  string = """
p: {0}
q: {1}
N: {2}
e: {3}
d: {4}""".format(p, q, N, e, d)
  return string
