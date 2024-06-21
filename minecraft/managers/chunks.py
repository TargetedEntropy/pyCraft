from math import floor

from ..networking.packets import clientbound

class ChunksManager:

    def __init__(self, data_manager):
        self.data = data_manager
        self.chunks = {}
        self.biomes = {}
        
    def handle_block(self, block_packet):
        self.set_block_at(block_packet.location.x, block_packet.location.y, block_packet.location.z, block_packet.block_state_id)
        #self.print_chunk(self.get_chunk(floor(block_packet.location.x/16), floor(block_packet.location.y/16), floor(block_packet.location.z/16)), block_packet.location.y%16)
        #print('Block %s at %s'%(blocks_states[block_packet.block_state_id], block_packet.location))

    def handle_multiblock(self, multiblock_packet):
        for b in multiblock_packet.records:
            self.handle_block(b)

    def handle_chunk(self, chunk_packet):
        print(f"Chunk: {chunk_packet}")
        for i in chunk_packet.chunks:
            self.chunks[(chunk_packet.x, i, chunk_packet.z)] = chunk_packet.chunks[i]        
        self.biomes[(chunk_packet.x, None, chunk_packet.z)] = chunk_packet.biomes # FIXME

    def register(self, connection):
     #   connection.register_packet_listener(self.handle_block, clientbound.play.BlockChangePacket)
      #  connection.register_packet_listener(self.handle_multiblock, clientbound.play.MultiBlockChangePacket)
        connection.register_packet_listener(self.handle_chunk, clientbound.play.ChunkDataPacket)

    def get_chunk(self, x, y, z):
        index = (x, y, z)
        if not index in self.chunks:
            raise ChunkNotLoadedException(index)
        return self.chunks[index]

    def get_loaded_area(self, ignore_empty=False):
        first = next(iter(self.chunks.keys()))
        x0 = x1 = first[0]
        y0 = y1 = first[1]
        z0 = z1 = first[2]
        for k in self.chunks.keys():
            if ignore_empty and self.chunks[k].empty:
                continue
            x0 = min(x0, k[0])
            x1 = max(x1, k[0])
            y0 = min(y0, k[1])
            y1 = max(y1, k[1])
            z0 = min(z0, k[2])
            z1 = max(z1, k[2])
        return ((x0,y0,z0),(x1,y1,z1))

    def get_block_at(self, x, y, z):
        c = self.get_chunk(floor(x/16), floor(y/16), floor(z/16))
        return c.get_block_at(x%16, y%16, z%16)

    def set_block_at(self, x, y, z, block):
        c = self.get_chunk(floor(x/16), floor(y/16), floor(z/16))
        c.set_block_at(x%16, y%16, z%16, block)

    def print_chunk(self, chunk, y_slice):
        print("This is chunk %d %d %d at slice %d:"%(chunk.x, chunk.y, chunk.z, y_slice))
        print("+%s+"%("-"*16))
        # for z in range(16):
        #     missing = []
        #     print("|", end="")
        #     for x in range(16):
        #         sid = chunk.get_block_at(x, y_slice, z)
        #         bloc = self.data.blocks_states[sid]
        #         if bloc == "minecraft:air" or bloc == "minecraft:cave_air":
        #             c = " "
        #         elif bloc == "minecraft:grass_block" or bloc == "minecraft:dirt":
        #             c = "-"
        #         elif bloc == "minecraft:water":
        #             c = "~"
        #         elif bloc == "minecraft:lava":
        #             c = "!"
        #         elif bloc == "minecraft:bedrock":
        #             c = "_"
        #         elif bloc == "minecraft:stone":
        #             c = "X"
        #         else:
        #             missing.append(bloc)
        #             c = "?"

        #         print(c, end="")
        #     print("|  %s"%(",".join(missing)))
        # print("+%s+"%("-"*16))
        if chunk.entities:
            print("Entities in slice: %s"%(", ".join([x['id'].decode() for x in chunk.entities])))


class ChunkNotLoadedException(Exception):
    def __str__(self):
        pos = self.args[0]
        return "Chunk at %d %d %d not loaded (yet?)"%(pos[0], pos[1], pos[2])

