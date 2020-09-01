/*
 * Mycomparator.h
 *
 *  Created on: 23 mar 2020
 *      Author: Andrea
 */

#ifndef MYCOMPARATOR_H_
#define MYCOMPARATOR_H_

#include <omnetpp/cqueue.h>
#include <omnetpp/cmessage.h>
class Mycomparator: public omnetpp::cQueue::Comparator {
public:
    Mycomparator();
        virtual ~Mycomparator();
        virtual bool less(omnetpp::cObject *a, omnetpp::cObject *b);
        virtual omnetpp::cQueue::Comparator* dup() const;
};

#endif /* MYCOMPARATOR_H_ */
