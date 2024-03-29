/* Copyright (c) 2007 Scott Lembcke
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

// The spatial hash is Chipmunk's default (and currently only) spatial index type.
// Based on a chained hash table.

// Used internally to track objects added to the hash
typedef struct cpHandle{
	// Pointer to the object
	void *obj;
	// Retain count
	int retain;
	// Query stamp. Used to make sure two objects
	// aren't identified twice in the same query.
	int stamp;
} cpHandle;

// Linked list element for in the chains.
typedef struct cpSpaceHashBin{
	cpHandle *handle;
	struct cpSpaceHashBin *next;
} cpSpaceHashBin;

// BBox callback. Called whenever the hash needs a bounding box from an object.
typedef cpBB (*cpSpaceHashBBFunc)(void *obj);

typedef struct cpSpaceHash{
	// Number of cells in the table.
	int numcells;
	// Dimentions of the cells.
	cpFloat celldim;
	
	// BBox callback.
	cpSpaceHashBBFunc bbfunc;

	// Hashset of all the handles.
	cpHashSet *handleSet;
	
	cpSpaceHashBin **table;
	// List of recycled bins.
	cpSpaceHashBin *bins;

	// Incremented on each query. See cpHandle.stamp.
	int stamp;
} cpSpaceHash;

//Basic allocation/destruction functions.
cpSpaceHash *cpSpaceHashAlloc(void);
cpSpaceHash *cpSpaceHashInit(cpSpaceHash *hash, cpFloat celldim, int cells, cpSpaceHashBBFunc bbfunc);
cpSpaceHash *cpSpaceHashNew(cpFloat celldim, int cells, cpSpaceHashBBFunc bbfunc);

void cpSpaceHashDestroy(cpSpaceHash *hash);
void cpSpaceHashFree(cpSpaceHash *hash);

// Resize the hashtable. (Does not rehash! You must call cpSpaceHashRehash() if needed.)
void cpSpaceHashResize(cpSpaceHash *hash, cpFloat celldim, int numcells);

// Add an object to the hash.
void cpSpaceHashInsert(cpSpaceHash *hash, void *obj, unsigned long id, cpBB bb);
// Remove an object from the hash.
void cpSpaceHashRemove(cpSpaceHash *hash, void *obj, unsigned long id);

// Iterator function
typedef void (*cpSpaceHashIterator)(void *obj, void *data);
// Iterate over the objects in the hash.
void cpSpaceHashEach(cpSpaceHash *hash, cpSpaceHashIterator func, void *data);

// Rehash the contents of the hash.
void cpSpaceHashRehash(cpSpaceHash *hash);
// Rehash only a specific object.
void cpSpaceHashRehashObject(cpSpaceHash *hash, void *obj, unsigned long id);

// Query callback.
typedef int (*cpSpaceHashQueryFunc)(void *obj1, void *obj2, void *data);
// Query the hash for a given BBox.
void cpSpaceHashQuery(cpSpaceHash *hash, void *obj, cpBB bb, cpSpaceHashQueryFunc func, void *data);
// Run a query for the object, then insert it. (Optimized case)
void cpSpaceHashQueryInsert(cpSpaceHash *hash, void *obj, cpBB bb, cpSpaceHashQueryFunc func, void *data);
// Rehashes while querying for each object. (Optimized case) 
void cpSpaceHashQueryRehash(cpSpaceHash *hash, cpSpaceHashQueryFunc func, void *data);
