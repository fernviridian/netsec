#!/usr/bin/python

from Crypto.Hash import SHA256

import prob01
import prob02
import prob03
import prob04
import prob05
import prob06
import prob07

def sha256(msg):
  return SHA256.new(msg).hexdigest()

known_hashes = {}

def load_hashes():
  hashes = {}
  hash_filename = "hashes.txt"
  for line in file(hash_filename):
    toks = line.strip().split()
    if len(toks) != 2: continue
    h = toks[0]
    msg = toks[1]
    hashes[msg] = h
  return hashes

def get_hash(msg):
  global known_hashes
  if msg not in known_hashes:
    known_hashes = load_hashes()
  return known_hashes[msg]    

def load_flags(flag_filename):
  flags = {}
  for line in file(flag_filename):
    print "Read line [%s]" % line.strip()
    toks = line.strip().split()
    if len(toks) != 2:
      continue
    if not "FLAG" in toks[0]:
      continue
    flag_id = toks[0]
    the_flag = line
    flags[flag_id] = the_flag
  print "Found flags =", flags
  return flags


def verify_flag(flag, flagnum):
  # First a sanity check for proper formatting
  # The flag should look something like "FLAG abcd1234..."
  toks = flag.split()
  assert "FLAG" in toks[0]
  # Second, make sure we're consistent with newlines.
  # When the flag comes from a file, it'll be there.
  # It's easiest if we ensure that this is always the case.
  # So when it's missing, we just add it here before the hash.
  if not flag.endswith("\n"):
    flag += "\n"
  # Compute the hash of our candidate flag
  my_hash = sha256(flag)
  # Load the correct hash from our hashes file
  filename = "flag%02d.txt" % flagnum
  h = get_hash(filename)
  # The two hashes should be identical
  assert my_hash == h

def verify_flag_file(flagnum, label="FLAG"):
  filename = "flag%02d.txt" % flagnum
  flags = load_flags(filename)
  flag = flags[label]
  verify_flag(flag, flagnum)


# Check the saved flags 
# They should be stored in files named flag??.txt

def test_flag01():
  verify_flag_file(1)

def test_flag02():
  verify_flag_file(2)

def test_flag03():
  verify_flag_file(3)

def test_flag04():
  verify_flag_file(4)

def test_flag05():
  verify_flag_file(5)

def test_flag06():
  verify_flag_file(6)

def test_flag07():
  verify_flag_file(7)



# Check the code that gets the flag for each problem
# Each file should define a get_flag() function

def test_prob01():
  flag = prob01.get_flag()
  verify_flag(flag, 1)

def test_prob02():
  flag = prob02.get_flag()
  verify_flag(flag, 2)

def test_prob03():
  flag = prob03.get_flag()
  verify_flag(flag, 3)

def test_prob04():
  flag = prob04.get_flag()
  verify_flag(flag, 4)

def test_prob05():
  flag = prob05.get_flag()
  verify_flag(flag, 5)

def test_prob06():
  flag = prob06.get_flag()
  verify_flag(flag, 6)

def test_prob07():
  flag = prob07.get_flag()
  verify_flag(flag, 7)


