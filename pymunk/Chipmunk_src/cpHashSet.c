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
 
#include <stdlib.h>
#include <assert.h>

#include "chipmunk.h"
#include "prime.h"

void
cpHashSetDestroy(cpHashSet *set)
{
	// Free the chains.
	for(int i=0; i<set->size; i++){
		// Free the bins in the chain.
		cpHashSetBin *bin = set->table[i];
		while(bin){
			cpHashSetBin *next = bin->next;
			free(bin);
			bin = next;
		}
	}
	
	// Free the table.
	free(set->table);
}

void
cpHashSetFree(cpHashSet *set)
{
	if(set) cpHashSetDestroy(set);
	free(set);
}

cpHashSet *
cpHashSetAlloc(void)
{
	return calloc(1, sizeof(cpHashSet));
}

cpHashSet *
cpHashSetInit(cpHashSet *set, int size, cpHashSetEqlFunc eqlFunc, cpHashSetTransFunc trans)
{
	set->size = next_prime(size);
	set->entries = 0;
	
	set->eql = eqlFunc;
	set->trans = trans;
	
	set->default_value = NULL;
	
	set->table = calloc(set->size, sizeof(cpHashSetBin *));
	
	return set;
}

cpHashSet *
cpHashSetNew(int size, cpHashSetEqlFunc eqlFunc, cpHashSetTransFunc trans)
{
	return cpHashSetInit(cpHashSetAlloc(), size, eqlFunc, trans);
}

static int
setIsFull(cpHashSet *set)
{
	return (set->entries >= set->size);
}

static void
cpHashSetResize(cpHashSet *set)
{
	// Get the next approximate doubled prime.
	int newSize = next_prime(set->size + 1);
	// Allocate a new table.
	cpHashSetBin **newTable = calloc(newSize, sizeof(cpHashSetBin *));
	
	// Iterate over the chains.
	for(int i=0; i<set->size; i++){
		// Rehash the bins into the new table.
		cpHashSetBin *bin = set->table[i];
		while(bin){
			cpHashSetBin *next = bin->next;
			
			int index = bin->hash%newSize;
			bin->next = newTable[index];
			newTable[index] = bin;
			
			bin = next;
		}
	}
	
	free(set->table);
	
	set->table = newTable;
	set->size = newSize;
}

void *
cpHashSetInsert(cpHashSet *set, unsigned long hash, void *ptr, void *data)
{
	int index = hash%set->size;
	
	// Find the bin with the matching element.
	cpHashSetBin *bin = set->table[index];
	while(bin && !set->eql(ptr, bin->elt))
		bin = bin->next;
	
	// Create it necessary.
	if(!bin){
		bin = malloc(sizeof(cpHashSetBin));
		bin->hash = hash;
		bin->elt = set->trans(ptr, data); // Transform the pointer.
		
		bin->next = set->table[index];
		set->table[index] = bin;
		
		set->entries++;
		
		// Resize the set if it's full.
		if(setIsFull(set))
			cpHashSetResize(set);
	}
	
	return bin->elt;
}

void *
cpHashSetRemove(cpHashSet *set, unsigned long hash, void *ptr)
{
	int index = hash%set->size;
	
	// Pointer to the previous bin pointer.
	cpHashSetBin **prev_ptr = &set->table[index];
	// Pointer the the current bin.
	cpHashSetBin *bin = set->table[index];
	
	// Find the bin
	while(bin && !set->eql(ptr, bin->elt)){
		prev_ptr = &bin->next;
		bin = bin->next;
	}
	
	// Remove it if it exists.
	if(bin){
		// Update the previos bin pointer to point to the next bin.
		(*prev_ptr) = bin->next;
		set->entries--;
		
		void *return_value = bin->elt;
		free(bin);
		return return_value;
	}
	
	return NULL;
}

void *
cpHashSetFind(cpHashSet *set, unsigned long hash, void *ptr)
{	
	int index = hash%set->size;
	cpHashSetBin *bin = set->table[index];
	while(bin && !set->eql(ptr, bin->elt))
		bin = bin->next;
		
	return (bin ? bin->elt : set->default_value);
}

void
cpHashSetEach(cpHashSet *set, cpHashSetIterFunc func, void *data)
{
	for(int i=0; i<set->size; i++){
		cpHashSetBin *bin;
		for(bin = set->table[i]; bin; bin = bin->next)
			func(bin->elt, data);
	}
}

void
cpHashSetReject(cpHashSet *set, cpHashSetRejectFunc func, void *data)
{
	// Iterate over all the chains.
	for(int i=0; i<set->size; i++){
		// The rest works similarly to cpHashSetRemove() above.
		cpHashSetBin **prev_ptr = &set->table[i];
		cpHashSetBin *bin = set->table[i];
		while(bin){
			cpHashSetBin *next = bin->next;
			
			if(func(bin->elt, data)){
				prev_ptr = &bin->next;
			} else {
				(*prev_ptr) = next;

				set->entries--;
				free(bin);
			}
			
			bin = next;
		}
	}
}
