(* a datatype specifically for 32-byte blocks, (like hashes).
 * implements the ORD_KEY siganture, meaning it has compare. 
 * Can be converted to and from a vector of Word8.word.
 * Can be converted to a List of Word8.word. 
 *
 * All operations are constant time.
 * Stored in constant space.
 *)
structure Bytes32 : ORD_KEY = struct
  datatype bytes32 = Bytes32 of (
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word *
    Word8.word * Word8.word * Word8.word * Word8.word)
  type ord_key = bytes32
  fun fromVec (x : Word8.word vector) : bytes32 = Bytes32 (
    sub x 0 , sub x 1 , sub x 2 , sub x 3 , 
    sub x 4 , sub x 5 , sub x 6 , sub x 7 , 
    sub x 8 , sub x 9 , sub x 10, sub x 11, 
    sub x 12, sub x 13, sub x 14, sub x 15, 
    sub x 16, sub x 17, sub x 18, sub x 19, 
    sub x 20, sub x 21, sub x 22, sub x 23, 
    sub x 24, sub x 25, sub x 26, sub x 27, 
    sub x 28, sub x 29, sub x 30, sub x 31) 
  fun toList ((Bytes32 (x0 , x1 , x2 , x3 ,
                        x4 , x5 , x6 , x7 ,
                        x8 , x9 , x10, x11,
                        x12, x13, x14, x15,
                        x16, x17, x18, x19,
                        x20, x21, x22, x23,
                        x24, x25, x26, x27,
                        x28, x29, x30, x31)) : bytes32) : Word8.word list =
    [x0 , x1 , x2 , x3 ,
     x4 , x5 , x6 , x7 ,
     x8 , x9 , x10, x11,
     x12, x13, x14, x15,
     x16, x17, x18, x19,
     x20, x21, x22, x23,
     x24, x25, x26, x27,
     x28, x29, x30, x31]
  fun toVec (x : bytes32) : Word8.word vector = Vector.fromList (toList x)
  fun compare ((x,y) : bytes32 * bytes32) : order =
    collate Word8.compare (toList x, toList y)
end
