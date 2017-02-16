#include<math.h>

#include "m_pd.h"
#include<stdio.h>

#define Pi 3.14159265
#define N 3
#define Lx 1
#define Ly 1
#define Lz 1

static t_class *torN_class;

typedef struct _torN {
    t_object x_obj;
    t_outlet *size_out, *ang_out, *dist_out;
} t_torN;


float azimute (float x, float y , float z) {
    return atan2(x,y)*Pi/180.;
}


float elevation (float x, float y , float z) {
    float xy = sqrt( x*x +y*y);
    return atan2(xy,z)*Pi/180.;
}


float distance (float x, float y , float z) {
    return sqrt( x*x +y*y+z*z);
}

int torN(t_torN *b, t_float x, t_float y, t_float z) {
    int i, j, k = 0;
    double dist, ang;
    for(i = 0; i < N; i++){
        for(j = 0; j < N; j++){
            for(k = 0; k < N; k++){
                x = x+i*Lx-N/2; y = y+j*Ly-N/2; z = z+k*Lz-N/2;
                outlet_float(b->ang_out, (float) azimute(x,y,z));
                outlet_float(b->dist_out, (float) elevation(x,y,z));
                outlet_float(b->size_out, (float) distance(x,y,z));
            }
        }
    }
    return 0;
}


void *torN_new(void)
{  
  t_torN *x = (t_torN *)pd_new(torN_class);
    x->ang_out = outlet_new(&x->x_obj, &s_float);
    x->dist_out = outlet_new(&x->x_obj, &s_float);
    x->size_out = outlet_new(&x->x_obj, &s_float);
  return (void *)x;  
}  

void torN_bang(t_torN *x) {}


void torN_setup(void) {  
    torN_class = class_new(gensym("torN"), (t_newmethod)torN_new,
        0, sizeof(t_torN), CLASS_DEFAULT, 0);
    class_addbang(torN_class, torN_bang);
    class_addmethod(torN_class, (t_method)torN, gensym("torN"), A_DEFFLOAT, A_DEFFLOAT, A_DEFFLOAT, 0);
}


