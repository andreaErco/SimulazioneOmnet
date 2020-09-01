/*
 * Mycomparator.cc
 *
 *  Created on: 23 mar 2020
 *      Author: Andrea
 */

#include "Mycomparator.h"

Mycomparator::Mycomparator() {
    // TODO Auto-generated constructor stub

}

Mycomparator::~Mycomparator() {
    // TODO Auto-generated destructor stub
}

bool Mycomparator::less(omnetpp::cObject *a, omnetpp::cObject *b) {

        omnetpp::cMessage *msg = (omnetpp::cMessage *)(a);
        omnetpp::cMessage *mymsg = (omnetpp::cMessage *)(b);
        double val1=msg->par("Tempo di servizio").doubleValue();
        double val2=mymsg->par("Tempo di servizio").doubleValue();
        //std::cout<<"VALORE COMPARATOR : "<<val1<< std::endl;
        return val1<val2;
}

omnetpp::cQueue::Comparator* Mycomparator::dup() const {
    Mycomparator* p =new Mycomparator();
       return p;
}
