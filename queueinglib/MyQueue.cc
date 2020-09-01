//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 2006-2015 OpenSim Ltd.
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//

#include "MyQueue.h"
#include "Job.h"

namespace queueing {

Define_Module(MyQueue);

MyQueue::MyQueue()
{
    jobServiced = nullptr;
    endServiceMsg = nullptr;
}

MyQueue::~MyQueue()
{
    delete jobServiced;
    cancelAndDelete(endServiceMsg);
}

void MyQueue::initialize()
{
    droppedSignal = registerSignal("dropped");
    queueingTimeSignal = registerSignal("queueingTime");
    queueLengthSignal = registerSignal("queueLength");
    emit(queueLengthSignal, 0);
    busySignal = registerSignal("busy");
    emit(busySignal, false);

    endServiceMsg = new cMessage("end-service");
    fifo = par("fifo");
    capacity = par("capacity");
    queue.setName("queue");
    serviceTimeVec.setName("serviceTime:vector");
    Mycomparator * clone = new Mycomparator();
    queue.setup(clone);
}



void MyQueue::handleMessage(cMessage *msg)
{


    if (msg == endServiceMsg) {
        endService(jobServiced);
        if (queue.isEmpty()) {
            jobServiced = nullptr;
            emit(busySignal, false);
        }
        else {
            jobServiced = getFromQueue();
            emit(queueLengthSignal, length());


            /*******************************************************************************/
            simtime_t serviceTime;
            cMsgPar * par;
            try{
                double parServiceTime;
                par = &(jobServiced->par("Tempo di servizio"));
                parServiceTime =par->doubleValue();

                //serviceTime.setRaw(parServiceTime);

                //std::cout<<"Super MANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN 000000 : "<<serviceTime<<endl ;
                //std::cout<<"Super MANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN 111111100000000000000000 : "<<simTime()<<endl ;

                //serviceTimeVec.record(serviceTime);

                scheduleAt(simTime()+serviceTime, endServiceMsg);
                return;
            }catch(cRuntimeError e){
                serviceTime =startService(jobServiced);
                double valore = serviceTime.dbl();
                cMsgPar * parametro = &(msg->addPar("Tempo di servizio"));
                parametro->setDoubleValue(valore);
                //std::cout<<"paramtro set 1: "<<valore<< std::endl ;
                //std::cout<<"primo if 2"<<serviceTime<<endl ;
                //std::cout<<"ID VALORE"<<msg->getId()<< std::endl ;
                //std::cout<<"STMAPA VALORE"<<valore<< std::endl ;
                serviceTimeVec.record(serviceTime);
                scheduleAt(simTime()+serviceTime, endServiceMsg);
            }}
    }
    else {
        Job *job = check_and_cast<Job *>(msg);
        arrival(job);

        if (!jobServiced) {
            // processor was idle
            jobServiced = job;
            emit(busySignal, true);


            /*******************************************************************************/
            simtime_t serviceTime;
            cMsgPar * par;
            try{
                double parServiceTime;
                par = &(jobServiced->par("Tempo di servizio"));
                parServiceTime =par->doubleValue();


                //serviceTime.setRaw(parServiceTime);
                //serviceTimeVec.record(serviceTime);
                //std::cout<<"Super MANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN 1111111 : "<<serviceTime<<endl ;
               // std::cout<<"Super MANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN 111111100000000000000000 : "<<simTime()<<endl ;

                //std::cout<<"secondo if 1"<<serviceTime<<endl ;
                scheduleAt(simTime()+serviceTime, endServiceMsg);
                return;
            }catch(cRuntimeError e){}
            serviceTime =startService(jobServiced);
            double valore = serviceTime.dbl();
            cMsgPar * parametro = &(msg->addPar("Tempo di servizio"));
            parametro->setDoubleValue(valore);
            //std::cout<<"paramtro settato 2: "<<valore<< std::endl ;
            //std::cout<<"STMAPA VALORE"<<valore<< std::endl ;
            serviceTimeVec.record(serviceTime);

            //std::cout<<"secondo if 2"<<serviceTime<<endl ;
            scheduleAt(simTime()+serviceTime, endServiceMsg);

        }
        else {
            // check for container capacity
            if (capacity >= 0 && queue.getLength() >= capacity) {
                EV << "Capacity full! Job dropped.\n";
                if (hasGUI())
                    bubble("Dropped!");
                emit(droppedSignal, 1);
                delete job;
                return;
            }
            /*******************************************************************************/
            simtime_t serviceTime =startService(jobServiced);
            //std::cout<<serviceTime<<endl ;
            double valore = serviceTime.dbl();
            cMsgPar * parametro = &(msg->addPar("Tempo di servizio"));
            parametro->setDoubleValue(valore);
            //std::cout<<"paramtro Fine di tutto : "<<valore<< std::endl ;
            serviceTimeVec.record(serviceTime);
            queue.insert(job);
            emit(queueLengthSignal, length());
            job->setQueueCount(job->getQueueCount() + 1);
        }
    }
}


void MyQueue::refreshDisplay() const
{
    getDisplayString().setTagArg("i2", 0, jobServiced ? "status/execute" : "");
    getDisplayString().setTagArg("i", 1, queue.isEmpty() ? "" : "cyan");
}

Job *MyQueue::getFromQueue()
{
    Job *job;
    if (fifo) {
        job = (Job *)queue.pop();
    }
    else {
        job = (Job *)queue.back();
        // FIXME this may have bad performance as remove uses linear search
        queue.remove(job);
    }
    return job;
}

int MyQueue::length()
{
    return queue.getLength();
}

void MyQueue::arrival(Job *job)
{
    job->setTimestamp();
}

simtime_t MyQueue::startService(Job *job)
{
    // gather queueing time statistics
    simtime_t d = simTime() - job->getTimestamp();


    emit(queueingTimeSignal, d);
    job->setTotalQueueingTime(job->getTotalQueueingTime() + d);
    EV << "Starting service of " << job->getName() << endl;
    job->setTimestamp();

    double val =par("serviceTime").doubleValue();
    //std::cout<<"VALORE MYQUEUE (START SERVICE) : "<<val<< std::endl;

    return val ;
}

void MyQueue::endService(Job *job)
{
    EV << "Finishing service of " << job->getName() << endl;
    simtime_t d = simTime() - job->getTimestamp();
    job->setTotalServiceTime(job->getTotalServiceTime() + d);
    send(job, "out");
}

void MyQueue::finish()
{
}

}; //namespace

