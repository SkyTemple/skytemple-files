# Operations are encoded in command bytes (CMD):
# PHASE 1
CMD_1_ZERO_OUT      = 0x80  # All values below
CMD_1_FILL_OUT      = 0x80  # All values equal/above until next
CMD_1_COPY_BYTES    = 0xC0  # All values equal/above
# PHASE 2
CMD_2_SEEK_OFFSET   = 0x80  # All values below
CMD_2_FILL_LOW      = 0x80  # All values equal/above until next
CMD_2_COPY_LOW      = 0xC0  # All values equal/above
