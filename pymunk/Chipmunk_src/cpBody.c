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
#include <math.h>
#include <float.h>

#include "chipmunk.h"

cpBody*
cpBodyAlloc(void)
{
	return malloc(sizeof(cpBody));
}

cpBody*
cpBodyInit(cpBody *body, cpFloat m, cpFloat i)
{
	cpBodySetMass(body, m);
	cpBodySetMoment(body, i);

	body->p = cpvzero;
	body->v = cpvzero;
	body->f = cpvzero;
	
	cpBodySetAngle(body, 0.0f);
	body->w = 0.0f;
	body->t = 0.0f;
	
	body->v_bias = cpvzero;
	body->w_bias = 0.0f;
	
//	body->active = 1;

	return body;
}

cpBody*
cpBodyNew(cpFloat m, cpFloat i)
{
	return cpBodyInit(cpBodyAlloc(), m, i);
}

void cpBodyDestroy(cpBody *body){}

void
cpBodyFree(cpBody *body)
{
	if(body) cpBodyDestroy(body);
	free(body);
}

void
cpBodySetMass(cpBody *body, cpFloat m)
{
	body->m = m;
	body->m_inv = 1.0f/m;
}

void
cpBodySetMoment(cpBody *body, cpFloat i)
{
	body->i = i;
	body->i_inv = 1.0f/i;
}

void
cpBodySetAngle(cpBody *body, cpFloat a)
{
	body->a = fmod(a, M_PI*2.0f);
	body->rot = cpvforangle(a);
}

void
cpBodySlew(cpBody *body, cpVect pos, cpFloat dt)
{
	cpVect delta = cpvsub(body->p, pos);
	body->v = cpvmult(delta, 1.0/dt);
}

void
cpBodyUpdateVelocity(cpBody *body, cpVect gravity, cpFloat damping, cpFloat dt)
{
	body->v = cpvadd(cpvmult(body->v, damping), cpvmult(cpvadd(gravity, cpvmult(body->f, body->m_inv)), dt));
	body->w = body->w*damping + body->t*body->i_inv*dt;
}

void
cpBodyUpdatePosition(cpBody *body, cpFloat dt)
{
	body->p = cpvadd(body->p, cpvmult(cpvadd(body->v, body->v_bias), dt));
	cpBodySetAngle(body, body->a + (body->w + body->w_bias)*dt);
	
	body->v_bias = cpvzero;
	body->w_bias = 0.0f;
}

void
cpBodyResetForces(cpBody *body)
{
	body->f = cpvzero;
	body->t = 0.0f;
}

void
cpBodyApplyForce(cpBody *body, cpVect f, cpVect r)
{
	body->f = cpvadd(body->f, f);
	body->t += cpvcross(r, f);
}

void
cpDampedSpring(cpBody *a, cpBody *b, cpVect anchr1, cpVect anchr2, cpFloat rlen, cpFloat k, cpFloat dmp, cpFloat dt)
{
	// Calculate the world space anchor coordinates.
	cpVect r1 = cpvrotate(anchr1, a->rot);
	cpVect r2 = cpvrotate(anchr2, b->rot);
	
	cpVect delta = cpvsub(cpvadd(b->p, r2), cpvadd(a->p, r1));
	cpFloat dist = cpvlength(delta);
	cpVect n = dist ? cpvmult(delta, 1.0f/dist) : cpvzero;
	
	cpFloat f_spring = (dist - rlen)*k;

	// Calculate the world relative velocities of the anchor points.
	cpVect v1 = cpvadd(a->v, cpvmult(cpvperp(r1), a->w));
	cpVect v2 = cpvadd(b->v, cpvmult(cpvperp(r2), b->w));
	
	// Calculate the damping force.
	cpFloat vrn = cpvdot(cpvsub(v2, v1), n);
	cpFloat f_damp = vrn*cpfmin(dmp, 1.0f/(dt*(a->m_inv + b->m_inv)));
	
	// Apply!
	cpVect f = cpvmult(n, f_spring + f_damp);
	cpBodyApplyForce(a, f, r1);
	cpBodyApplyForce(b, cpvneg(f), r2);
}

//int
//cpBodyMarkLowEnergy(cpBody *body, cpFloat dvsq, int max)
//{
//	cpFloat ke = body->m*cpvdot(body->v, body->v);
//	cpFloat re = body->i*body->w*body->w;
//	
//	if(ke + re > body->m*dvsq)
//		body->active = 1;
//	else if(body->active)
//		body->active = (body->active + 1)%(max + 1);
//	else {
//		body->v = cpvzero;
//		body->v_bias = cpvzero;
//		body->w = 0.0f;
//		body->w_bias = 0.0f;
//	}
//	
//	return body->active;
//}
