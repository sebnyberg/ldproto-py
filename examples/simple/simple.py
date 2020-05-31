from proto import simple_pb2 as pb
from ldproto import write_ld, read_ld

user_addresses = {
  "Bob": [
    pb.Address(street="Baker's Street 1"),
    pb.Address(street="Champs-Élysées"),
  ],
  "Alice": [
    pb.Address(street="Bourbon Street"),
  ]
}

# Write two users to the file
with open('out.user.ld', 'wb') as f:
  for user_id in ['Bob', 'Alice']:
    pb_user = pb.User(id=user_id)
    pb_user.addresses.extend(user_addresses[user_id])

    write_ld(f, pb_user)

# Read users from the file, one by one
with open('out.user.ld', 'rb') as f:
  for pb_user in read_ld(f, pb.User):
    print(f"User: {pb_user.id}")
    for address in pb_user.addresses:
      print(f"Street: {address.street}")