# Operations are encoded in command bytes (CMD):
CMD_ZERO_OUT      = 0x80  # All values below
CMD_FILL_OUT      = 0x80  # All values equal/above until next
CMD_COPY_BYTES    = 0xC0  # All values equal/above
