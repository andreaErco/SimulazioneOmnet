//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//
import org.omnetpp.queueing.MyQueue;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;


//
// TODO documentation
//
network Network
{
    @display("bgb=485,313");
    submodules:
        source: Source {
            @display("p=96,215");
        }
        SPTF: MyQueue {
            @display("p=96,93");
        }
        queue: Queue {
            @display("p=362,93");
        }
        sink: Sink {
            @display("p=362,215");
        }
    connections:
        source.out --> SPTF.in++;
        SPTF.out --> queue.in++;
        queue.out --> sink.in++;
}

