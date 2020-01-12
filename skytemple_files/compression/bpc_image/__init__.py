# Operations are encoded in command bytes (CMD):
# BASE OPERATIONS
CMD_CP_FROM_POS                         = 0x80  # All values below: Copy from pos
# We build and copy a pattern:
CMD_CYCLE_PATTERN_AND_CP                = 0xE0  # All values equal/above
CMD_USE_LAST_PATTERN_AND_CP             = 0xC0  # All values equal/above until next
CMD_LOAD_BYTE_AS_PATTERN_AND_CP         = 0x80  # All values equal/above until next

# SPECIAL OPERATIONS (ALl values equal)
# Base operations, but the number of bytes to copy is stored in the next byte, not the CMD
CMD_CYCLE_PATTERN_AND_CP__NEXT          = 0xFF
CMD_USE_LAST_PATTERN_AND_CP__NEXT       = 0xDF
CMD_LOAD_BYTE_AS_PATTERN_AND_CP__NEXT   = 0xBF
CMD_CP_FROM_POS__NEXT                   = 0x7E
# In list for if:
CMD__NEXT = [CMD_CP_FROM_POS__NEXT, CMD_CYCLE_PATTERN_AND_CP__NEXT, CMD_LOAD_BYTE_AS_PATTERN_AND_CP__NEXT, CMD_USE_LAST_PATTERN_AND_CP__NEXT]
# Like above, but with the next 16-bit LE int:
CMD_COPY__NEXT__LE_16                   = 0x7F
