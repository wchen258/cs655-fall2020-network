#include <fcntl.h>
#include <netinet/in.h>
#include <sys/file.h>
#include <sys/time.h>
#include <sys/types.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

/* ******************************************************************
   ARQ NETWORK EMULATOR: VERSION 1.1  J.F.Kurose
   MODIFIED by Chong Wang on Oct.21,2005 for csa2,csa3 environments

   This code should be used for PA2, unidirectional data transfer protocols
   (from A to B)
   Network properties:
   - one way network delay averages five time units (longer if there
     are other messages in the channel for Pipelined ARQ), but can be larger
   - packets can be corrupted (either the header or the data portion)
     or lost, according to user-defined probabilities
   - packets will be delivered in the order in which they were sent
     (although some can be lost).
**********************************************************************/

/* a "msg" is the data unit passed from layer 5 (teachers code) to layer  */
/* 4 (students' code).  It contains the data (characters) to be delivered */
/* to layer 5 via the students transport level protocol entities.         */
struct msg
{
    char data[20];
};

/* a packet is the data unit passed from layer 4 (students code) to layer */
/* 3 (teachers code).  Note the pre-defined packet structure, which all   */
/* students must follow. */
struct pkt
{
    int seqnum;
    int acknum;
    int checksum;
    char payload[20];
    int sack[5] = {-1, -1, -1, -1, -1}; // initialized to -1 to indicate no history
};

/*- Your Definitions
  ---------------------------------------------------------------------------*/

/* Please use the following values in your program */

#define A 0
#define B 1
#define FIRST_SEQNO 0

/*- Declarations ------------------------------------------------------------*/
void restart_rxmt_timer(void);
void tolayer3(int AorB, pkt packet);
void tolayer5(char datasent[20]);

void starttimer(int AorB, double increment);
void stoptimer(int AorB);

/* WINDOW_SIZE, RXMT_TIMEOUT and TRACE are inputs to the program;
   Please set an appropriate value for LIMIT_SEQNO.
   You have to use these variables in your
   routines --------------------------------------------------------------*/

extern int WINDOW_SIZE; // size of the window
extern int
    LIMIT_SEQNO;            // when sequence number reaches this value, it wraps around
extern double RXMT_TIMEOUT; // retransmission timeout
extern int TRACE;           // trace level, for your debug purpose
extern double time_now;     // simulation time, for your debug purpose

/********* YOU MAY ADD SOME ROUTINES HERE ********/

typedef unsigned char byte;

struct stat
{
    int origin_A = 0; // num of origin pkt trans by A
    int next_valid_trans_A = FIRST_SEQNO;
    int retrans_A = 0;
    int deliver_B = 0;
    int ack_B = 0;
    int corrupt = 0;
    vector<double> rtts;
    vector<double> cmts;
    deque<pair<pkt, double>> traced;
    deque<pair<pkt, double>> traced_cmt;
};

enum {
    ORIGIN_A, RETRAN_A, DELIVER_B, ACK_B, CORRUPT,
    TRACE_PKT, UNTRACE, INPUT_A, TIMEOUT, INPUT_A_CMT,
    INPUT_A_RTT
};

/**  checksum computation */
byte get_checksum(void *p, int length)
{
    byte *s = (byte *)p, result = 0;
    for (int i = 0; i < length; ++i)
        result += s[i];
    return result;
}

unsigned wrap_add(unsigned n1, unsigned n2, unsigned period)
{
    return (n1 + n2) % period;
}

unsigned wrap_sub(unsigned n1, unsigned n2, unsigned period)
{
    return (n1 + period - n2) % period;
}



#define START_TIMER 0
#define PKT_CORRUPT 1

void print_message(int situation, pkt *packet)
{
    switch (situation)
    {
    case START_TIMER:
        cout << "\tStart timer at " << time_now << " planned inter at " << time_now + RXMT_TIMEOUT << endl;
        break;
    case PKT_CORRUPT:
        cout << "\tPkt corrupted, "
             << "packet checksum " << packet->checksum << " actual " << (unsigned int)get_checksum(packet, sizeof(pkt)) << endl;

    default:
        break;
    }
}

/** variables for A */
deque<pkt> A_queue;                   // A's linear buffer, [0:WINDOW_SIZE] for packets sent but
                                      // not ACKed, [WINDOW_SIZE:] for packets wait to be sent
unsigned first_unacked = FIRST_SEQNO; // sequence number of A_deque[0]

/** veriables for B */
deque<int> B_sack; // initialized to be size five, val=-1, and always keeps size=5

vector<pair<bool, char[20]>>
    B_window; // B's cicular buffer (length is WINDOW_SIZE), for packets
              // received but not delivered
unsigned next_expected =
    FIRST_SEQNO; // sequence number of the next expected packet
unsigned next_expected_index =
    0; // index of the next expected packet in B_window

    
struct stat s;


bool inWindow(int first_unacked, int seqno)
{
    int max_seqno = wrap_add(first_unacked, WINDOW_SIZE, LIMIT_SEQNO);
    if (max_seqno < first_unacked)
    {
        return (seqno >= max_seqno && seqno < first_unacked) ? false : true;
    }
    else
        return (seqno >= max_seqno || seqno < first_unacked) ? false : true;
}



void collect_stat(stat *s, int evt, pkt *packet, double time_now = 0.0)
{
    int tracker;
    switch (evt)
    {
    case ORIGIN_A:
        s->origin_A++;
        break;
    case RETRAN_A:
        s->retrans_A++;
        break;
    case DELIVER_B:
        s->deliver_B++;
        break;
    case ACK_B:
        s->ack_B++;
        break;
    case CORRUPT:
        s->corrupt++;
        break;
    case TRACE_PKT: // for rtt & cmt calc
        s->traced.push_back(make_pair(*packet, time_now));
        s->traced_cmt.push_back(make_pair(*packet, time_now));
        break;
    case INPUT_A_CMT:
        for(int k=0;k<5;k++){
            if (!s->traced_cmt.size())
            break;
            int packno = packet->sack[k];
            if(!inWindow(first_unacked, packno) || packno==-1) continue;
            for (int i = 0; i < (s->traced_cmt).size(); i++)
            {
                struct pkt p = s->traced_cmt[i].first;
                if (packno == p.seqnum)
                {
                    double previous_time = s->traced_cmt[i].second;
                    s->cmts.push_back(time_now - previous_time);
                    tracker = i;
                    s->traced_cmt.erase(s->traced_cmt.begin(), s->traced_cmt.begin() + tracker + 1);
                    break;
                }
            }
        }
        break;
    case INPUT_A_RTT:
        // try to find whether the packet received presents in the traced deque
        // if so, return the index, else keep -1
        int index=-1;
        for(int i=0; i<s->traced.size();i++){
            if(s->traced[i].first.seqnum==wrap_sub(packet->acknum, 1, LIMIT_SEQNO)
                && inWindow(first_unacked, packet->seqnum)) {
                    index = i;
                    break;
                }
        }

        // if does find it, it should: the eligible packe to calc RTT, and delete all the pkts in traced before this
        // due to channel does not reorder pkt
        // if didn't find it, we ignore 


    case INPUT_A: // for rtt calc
        if (!s->traced.size())
            break;
        if (wrap_sub(packet->acknum,1, LIMIT_SEQNO) == s->traced.front().first.seqnum)
        {
            double interval = time_now - s->traced.front().second;
            if (interval < RXMT_TIMEOUT)
            {
                s->rtts.push_back(time_now - s->traced.front().second);
            }
            s->traced.pop_front();
        }
        else
        {
            tracker = 0;
            for (int i = 0; i < (s->traced).size(); i++)
            {
                struct pkt p = s->traced[i].first;
                if (wrap_sub(packet->acknum,1, LIMIT_SEQNO) == p.seqnum)
                {
                    tracker = i;
                    break;
                }
            }
            s->traced.erase(s->traced.begin(), s->traced.begin() + tracker + 1);
        }
        break;
    case TIMEOUT:
        if (!s->traced.size())
            break;
        tracker = 0;
        for (int i = 0; i < (s->traced).size(); i++)
        {
            struct pkt p = s->traced[i].first;
            if (packet->seqnum == p.seqnum)
            {
                tracker = i;
                break;
            }
        }
        s->traced.erase(s->traced.begin(), s->traced.begin() + tracker + 1);
        break;

    default:
        break;
    }
}


int push_history(int seqno_to_acknowledged, bool nodup) // push in the seqno not ackno
{   
    if(nodup){
        for(int i=0;i<5;i++) {
            if(B_sack[i]==seqno_to_acknowledged)
                return 0;
        }
    }
    B_sack.pop_front();
    B_sack.push_back(seqno_to_acknowledged);
    return B_sack.size() == 5 ? 0 : -1;
}

pkt make_pkt(const void *p_msg, int seq, int ack)
{
    pkt packet;
    packet.seqnum = seq;
    packet.acknum = ack;
    packet.checksum = 0;
    memcpy(packet.payload, p_msg, sizeof(msg));
    for (int i = 0; i < 5; i++)
    packet.sack[i] = B_sack[i]; // save acked seqno, NOT ackno which is seqno+1
    packet.checksum = (byte)~get_checksum(&packet, sizeof(pkt));
    return packet;
}

/********* STUDENTS WRITE THE NEXT SEVEN ROUTINES *********/

/** called from layer 5, passed the data to be sent to other side */
void A_output(msg message)
{
    cout << "\nA_output at time " << time_now << endl;
    cout << "\tMessage from A layer 5 " << string(message.data, 20);
    cout << "\tCurrent sender buffer size " << A_queue.size() << endl;
    unsigned queue_size = A_queue.size();
    unsigned seq = wrap_add(first_unacked, queue_size, LIMIT_SEQNO);
    pkt outpkt = make_pkt(&message, seq, 0);
    cout << "\tSeqno " << outpkt.seqnum << " expected ackno " << outpkt.seqnum + 1 << " checksum " << outpkt.checksum << endl;
    A_queue.push_back(outpkt);
    if (queue_size < WINDOW_SIZE)
    { // the new packet is within window
        cout << "\tFind an empty space in the sneder window. Send to layer3 " << endl;
        tolayer3(A, outpkt);
        collect_stat(&s, ORIGIN_A, &outpkt);
        collect_stat(&s, TRACE_PKT, &outpkt);
        if (!queue_size)
        { // if it's the first packet in the queue
            starttimer(A, RXMT_TIMEOUT);
            print_message(START_TIMER, NULL);
        }
    }
    else
    {
        cout << "\tSender window has not space. Buffer the packet." << endl;
    }
}


/** called from layer 3, when a packet arrives for layer 4 */
void A_input(pkt packet)
{
    cout << "\nA_input at time " << time_now << endl;
    if (get_checksum(&packet, sizeof(pkt)) == 0xFF)
    {
        cout << "\tChecksum confirmed " << (unsigned int)get_checksum(&packet, sizeof(pkt)) << endl;
        cout << "\tACKno " << packet.acknum << " first_unacked_no " << first_unacked << endl;
        int first_unacked_anchor = first_unacked; // need an anchor to check the valid window for the sender buffer
        stoptimer(A);
        // remove the acked pkt and advance first_unacked
        collect_stat(&s, INPUT_A_CMT, &packet);
        cout << "\tACKed history ";
        for(int i=0; i<5; i++)
            cout << packet.sack[i] << " ";
        cout << endl;
        if(wrap_sub(packet.acknum,1, LIMIT_SEQNO)==first_unacked) {
            collect_stat(&s, INPUT_A_RTT, &packet, time_now);
        }
        for (int i = 0; i < 5; i++)
        {
            int seqno_delete = packet.sack[i];
            if(seqno_delete==-1) continue; // during the very first ack from B, -1 to indicate no ack history 
            for (int k = 0; k < A_queue.size(); k++)
            {
                if (!inWindow(first_unacked_anchor, A_queue[k].seqnum))
                    break;
                if (seqno_delete == A_queue[k].seqnum)
                {
                    A_queue.erase(A_queue.begin() + k);
                    if (seqno_delete == first_unacked)
                        first_unacked = wrap_add(first_unacked, 1, LIMIT_SEQNO);
                    break;
                }
            }
        }
        // send to layer3 for all eligible packet
        
        int flag=false;
        for (int i = 0; i < A_queue.size(); i++)
        {
            if (inWindow(first_unacked, A_queue[i].seqnum))
            {
                tolayer3(A, A_queue[i]);
                if(!inWindow(first_unacked_anchor, A_queue[i].seqnum)) 
                {
                    collect_stat(&s, ORIGIN_A, &A_queue[i]);
                    collect_stat(&s, TRACE_PKT, &A_queue[i]);
                } else collect_stat(&s, RETRAN_A, &A_queue[i]);
                flag=true;
            }
            else
                break;
        }
        if (flag) {
            starttimer(A, RXMT_TIMEOUT);
            print_message(START_TIMER, NULL);
        }
    }
    else
    {
        collect_stat(&s, CORRUPT, NULL);
        print_message(PKT_CORRUPT, &packet);
    }
}

/** called when A's timer goes off */
void A_timerinterrupt(void)
{
    cout << "\nA_inter at time " << time_now << endl;
    for (int i = 0; i < A_queue.size(); i++)
        {
            if (inWindow(first_unacked, A_queue[i].seqnum))
            {
                tolayer3(A, A_queue[i]);
                collect_stat(&s, RETRAN_A, &A_queue[i]);
            }
            else
                break;
        }
    // collect_stat(&s, TIMEOUT, &A_queue.front());
    // collect_stat(&s, RETRAN_A, &A_queue.front());
    starttimer(A, RXMT_TIMEOUT);
    print_message(START_TIMER, NULL);
}

/** the following routine will be called once (only) before any other
 entity A routines are called. You can use it to do any initialization */
void A_init(void)
{
}

/** called from layer 3, when a packet arrives for layer 4 at B*/
void B_input(pkt packet)
{
    cout << "\nB_input at time " << time_now << endl;
    if (get_checksum(&packet, sizeof(pkt)) == 0xFF)
    {
        push_history(packet.seqnum, false);
        unsigned offset = wrap_sub(packet.seqnum, next_expected, LIMIT_SEQNO);
        if (offset < WINDOW_SIZE)
        { // within window
            unsigned index =
                wrap_add(next_expected_index, offset,
                         WINDOW_SIZE); // the place to buffer the packet
            if (!B_window[index].first)
            {                                 // new packet
                B_window[index].first = true; // mark as full
                memcpy(&B_window[index].second, packet.payload, sizeof(msg));
                if (!offset) // it's the expected packet
                    do
                    {
                        tolayer5(B_window[next_expected_index]
                                     .second); // in-order delivery
                        cout << "\tPkt delivered, seqno " << packet.seqnum << endl; 
                        collect_stat(&s, DELIVER_B, NULL);
                        B_window[next_expected_index].first =
                            false; // mark as empty
                        next_expected_index =
                            wrap_add(next_expected_index, 1, WINDOW_SIZE);
                        next_expected = wrap_add(next_expected, 1, LIMIT_SEQNO);
                    } while (B_window[next_expected_index].first);
            }
        }
        pkt ack =
            make_pkt(packet.payload, 0,
                     next_expected); // whether within window or not, send ack
        tolayer3(B, ack);
        cout << "\tAck sent to layer3 by B, ackno " << ack.acknum << endl;
        collect_stat(&s, ACK_B, &ack);
    }
    else{
        collect_stat(&s, CORRUPT, NULL);
        print_message(PKT_CORRUPT, &packet);
    }
}

/** the following rouytine will be called once (only) before any other
 entity B routines are called. You can use it to do any initialization */
void B_init(void)
{   
    B_window.resize(WINDOW_SIZE); 
    for (int i = 0; i < 5; i++)
        B_sack.push_back(-1);
}

/** called at end of simulation to print final statistics */
void Simulation_done(void)
{
    /* TO PRINT THE STATISTICS, FILL IN THE DETAILS BY PUTTING VARIBALE NAMES.
     * DO NOT CHANGE THE FORMAT OF PRINTED OUTPUT */
    float lost_ratio = ((float)s.retrans_A - s.corrupt) /
                       ((float)s.origin_A + s.retrans_A + s.ack_B);
    float corr_ratio = ((float)s.corrupt) /
                       ((float)s.origin_A + s.retrans_A + s.ack_B - s.retrans_A + s.corrupt);

    double rtt;
    for (auto &n : s.rtts)
        rtt += n;
    rtt /= s.rtts.size();

    double cmt_time;
    for (auto &n : s.cmts)
        cmt_time += n;
    cmt_time /= s.cmts.size();
    cout << "debug " << s.cmts.size() << endl;

    cout << "\n\n===============STATISTICS======================= \n"
         << endl;
    cout << "Number of original packets transmitted by A: " << s.origin_A << endl;
    cout << "Number of retransmissions by A: " << s.retrans_A << endl;
    cout << "Number of data packets delivered to layer 5 at B: " << s.deliver_B << endl;
    cout << "Number of ACK packets sent by B: " << s.ack_B << endl;
    cout << "Number of corrupted packets: " << s.corrupt << endl;
    cout << "Ratio of lost packets: " << lost_ratio << endl;
    cout << "Ratio of corrupted packets: " << corr_ratio << endl;
    cout << "Average RTT: " << rtt << endl;
    cout << "Average communication time: " << cmt_time << endl;
    cout << "==================================================" << endl;

    /* PRINT YOUR OWN STATISTIC HERE TO CHECK THE CORRECTNESS OF YOUR PROGRAM */
    // printf("\nEXTRA: \n");
    /* EXAMPLE GIVEN BELOW */
    /* printf("Example statistic you want to check e.g. number of ACK packets
     * received by A : <YourVariableHere>"); */
}

/*****************************************************************
***************** NETWORK EMULATION CODE STARTS BELOW ***********
The code below emulates the layer 3 and below network environment:
  - emulates the tranmission and delivery (possibly with bit-level corruption
    and packet loss) of packets across the layer 3/4 interface
  - handles the starting/stopping of a timer, and generates timer
    interrupts (resulting in calling students timer handler).
  - generates message to be sent (passed from later 5 to 4)

THERE IS NOT REASON THAT ANY STUDENT SHOULD HAVE TO READ OR UNDERSTAND
THE CODE BELOW.  YOU SHOLD NOT TOUCH, OR REFERENCE (in your code) ANY
OF THE DATA STRUCTURES BELOW.  If you're interested in how I designed
the emulator, you're welcome to look at the code - but again, you should have
to, and you defeinitely should not have to modify
******************************************************************/

struct event
{
    double evtime; /* event time */
    int evtype;    /* event type code */
    int eventity;  /* entity where event occurs */
    pkt *pktptr;   /* ptr to packet (if any) assoc w/ this event */
    struct event *prev;
    struct event *next;
};
struct event *evlist = NULL; /* the event list */

/* Advance declarations. */
void init(void);
void generate_next_arrival(void);
void insertevent(struct event *p);

/* possible events: */
#define TIMER_INTERRUPT 0
#define FROM_LAYER5 1
#define FROM_LAYER3 2

#define OFF 0
#define ON 1

int TRACE = 0; /* for debugging purpose */
FILE *fileoutput;
double time_now = 0.000;
int WINDOW_SIZE;
int LIMIT_SEQNO;
double RXMT_TIMEOUT;
double lossprob;    /* probability that a packet is dropped  */
double corruptprob; /* probability that one bit is packet is flipped */
double lambda;      /* arrival rate of messages from layer 5 */
int ntolayer3;      /* number sent into layer 3 */
int nlost;          /* number lost in media */
int ncorrupt;       /* number corrupted by media*/
int nsim = 0;
int nsimmax = 0;
unsigned int seed[5]; /* seed used in the pseudo-random generator */

int main(int argc, char **argv)
{
    struct event *eventptr;
    msg msg2give;
    pkt pkt2give;

    int i, j;

    init();
    A_init();
    B_init();

    while (1)
    {
        eventptr = evlist; /* get next event to simulate */
        if (eventptr == NULL)
            goto terminate;
        evlist = evlist->next; /* remove this event from event list */
        if (evlist != NULL)
            evlist->prev = NULL;
        if (TRACE >= 2)
        {
            printf("\nEVENT time: %f,", eventptr->evtime);
            printf("  type: %d", eventptr->evtype);
            if (eventptr->evtype == 0)
                printf(", timerinterrupt  ");
            else if (eventptr->evtype == 1)
                printf(", fromlayer5 ");
            else
                printf(", fromlayer3 ");
            printf(" entity: %d\n", eventptr->eventity);
        }
        time_now = eventptr->evtime; /* update time to next event time */
        if (eventptr->evtype == FROM_LAYER5)
        {
            generate_next_arrival(); /* set up future arrival */
            /* fill in msg to give with string of same letter */
            j = nsim % 26;
            for (i = 0; i < 20; i++)
                msg2give.data[i] = 97 + j;
            msg2give.data[19] = '\n';
            nsim++;
            if (nsim == nsimmax + 1)
                break;
            A_output(msg2give);
        }
        else if (eventptr->evtype == FROM_LAYER3)
        {
            pkt2give.seqnum = eventptr->pktptr->seqnum;
            pkt2give.acknum = eventptr->pktptr->acknum;
            pkt2give.checksum = eventptr->pktptr->checksum;
            /** wf need to deliver sack as well **/
            for (int k=0; k<5; k++)
                pkt2give.sack[k] = eventptr->pktptr->sack[k];
            /** done **/
            for (i = 0; i < 20; i++)
                pkt2give.payload[i] = eventptr->pktptr->payload[i];
            if (eventptr->eventity == A){ /* deliver packet by calling */
                A_input(pkt2give);       /* appropriate entity */
            }
            else
                B_input(pkt2give);
            free(eventptr->pktptr); /* free the memory for packet */
        }
        else if (eventptr->evtype == TIMER_INTERRUPT)
        {
            A_timerinterrupt();
        }
        else
        {
            printf("INTERNAL PANIC: unknown event type \n");
        }
        free(eventptr);
    }
terminate:
    Simulation_done(); /* allow students to output statistics */
    printf("Simulator terminated at time %.12f\n", time_now);
    return (0);
}

void init(void) /* initialize the simulator */
{
    int i = 0;
    printf("----- * Network Simulator Version 1.1 * ------ \n\n");
    printf("Enter number of messages to simulate: ");
    scanf("%d", &nsimmax);
    printf("Enter packet loss probability [enter 0.0 for no loss]:");
    scanf("%lf", &lossprob);
    printf("Enter packet corruption probability [0.0 for no corruption]:");
    scanf("%lf", &corruptprob);
    printf(
        "Enter average time between messages from sender's layer5 [ > 0.0]:");
    scanf("%lf", &lambda);
    printf("Enter window size [>0]:");
    scanf("%d", &WINDOW_SIZE);
    LIMIT_SEQNO = WINDOW_SIZE * 2; // set appropriately; here assumes SR
    printf("Enter retransmission timeout [> 0.0]:");
    scanf("%lf", &RXMT_TIMEOUT);
    printf("Enter trace level:");
    scanf("%d", &TRACE);
    printf("Enter random seed: [>0]:");
    scanf("%d", &seed[0]);
    for (i = 1; i < 5; i++)
        seed[i] = seed[0] + i;
    fileoutput = fopen("OutputFile", "w");
    if (!fileoutput)
        exit(1);
    ntolayer3 = 0;
    nlost = 0;
    ncorrupt = 0;
    time_now = 0.0;          /* initialize time to 0.0 */
    generate_next_arrival(); /* initialize event list */
}

/****************************************************************************/
/* mrand(): return a double in range [0,1].  The routine below is used to */
/* isolate all random number generation in one location.  We assume that the*/
/* system-supplied rand() function return an int in therange [0,mmm]        */
/*     modified by Chong Wang on Oct.21,2005                                */
/****************************************************************************/
int nextrand(int i)
{
    seed[i] = seed[i] * 1103515245 + 12345;
    return (unsigned int)(seed[i] / 65536) % 32768;
}

double mrand(int i)
{
    double mmm = 32767;    /* largest int  - MACHINE DEPENDENT!!!!!!!!   */
    double x;              /* individual students may need to change mmm */
    x = nextrand(i) / mmm; /* x should be uniform in [0,1] */
    if (TRACE == 0)
        printf("%.16f\n", x);
    return (x);
}

/********************* EVENT HANDLINE ROUTINES *******/
/*  The next set of routines handle the event list   */
/*****************************************************/
void generate_next_arrival(void)
{
    double x;
    struct event *evptr;

    if (TRACE > 2)
        printf("          GENERATE NEXT ARRIVAL: creating new arrival\n");

    x = lambda * mrand(0) * 2; /* x is uniform on [0,2*lambda] */
                               /* having mean of lambda        */
    evptr = (struct event *)malloc(sizeof(struct event));
    evptr->evtime = time_now + x;
    evptr->evtype = FROM_LAYER5;
    evptr->eventity = A;
    insertevent(evptr);
}

void insertevent(struct event *p)
{
    struct event *q, *qold;

    if (TRACE > 2)
    {
        printf("            INSERTEVENT: time is %f\n", time_now);
        printf("            INSERTEVENT: future time will be %f\n", p->evtime);
    }
    q = evlist; /* q points to header of list in which p struct inserted */
    if (q == NULL)
    { /* list is empty */
        evlist = p;
        p->next = NULL;
        p->prev = NULL;
    }
    else
    {
        for (qold = q; q != NULL && p->evtime > q->evtime; q = q->next)
            qold = q;
        if (q == NULL)
        { /* end of list */
            qold->next = p;
            p->prev = qold;
            p->next = NULL;
        }
        else if (q == evlist)
        { /* front of list */
            p->next = evlist;
            p->prev = NULL;
            p->next->prev = p;
            evlist = p;
        }
        else
        { /* middle of list */
            p->next = q;
            p->prev = q->prev;
            q->prev->next = p;
            q->prev = p;
        }
    }
}

void printevlist(void)
{
    struct event *q;
    printf("--------------\nEvent List Follows:\n");
    for (q = evlist; q != NULL; q = q->next)
    {
        printf("Event time: %f, type: %d entity: %d\n", q->evtime, q->evtype,
               q->eventity);
    }
    printf("--------------\n");
}

/********************** Student-callable ROUTINES ***********************/

/* called by students routine to cancel a previously-started timer */
void stoptimer(int AorB)
/* A or B is trying to stop timer */
{
    struct event *q /* ,*qold */;
    if (TRACE > 2)
        printf("          STOP TIMER: stopping timer at %f\n", time_now);
    /* for (q=evlist; q!=NULL && q->next!=NULL; q = q->next)  */
    for (q = evlist; q != NULL; q = q->next)
        if ((q->evtype == TIMER_INTERRUPT && q->eventity == AorB))
        {
            /* remove this event */
            if (q->next == NULL && q->prev == NULL)
                evlist = NULL;        /* remove first and only event on list */
            else if (q->next == NULL) /* end of list - there is one in front */
                q->prev->next = NULL;
            else if (q ==
                     evlist)
            { /* front of list - there must be event after */
                q->next->prev = NULL;
                evlist = q->next;
            }
            else
            { /* middle of list */
                q->next->prev = q->prev;
                q->prev->next = q->next;
            }
            free(q);
            return;
        }
    printf("Warning: unable to cancel your timer. It wasn't running.\n");
}

void starttimer(int AorB, double increment)
/* A or B is trying to stop timer */
{
    struct event *q;
    struct event *evptr;

    if (TRACE > 2)
        printf("          START TIMER: starting timer at %f\n", time_now);
    /* be nice: check to see if timer is already started, if so, then  warn */
    /* for (q=evlist; q!=NULL && q->next!=NULL; q = q->next)  */
    for (q = evlist; q != NULL; q = q->next)
        if ((q->evtype == TIMER_INTERRUPT && q->eventity == AorB))
        {
            printf(
                "Warning: attempt to start a timer that is already started\n");
            return;
        }

    /* create future event for when timer goes off */
    evptr = (struct event *)malloc(sizeof(struct event));
    evptr->evtime = time_now + increment;
    evptr->evtype = TIMER_INTERRUPT;
    evptr->eventity = AorB;
    insertevent(evptr);
}

/************************** TOLAYER3 ***************/
void tolayer3(int AorB, pkt packet)
/* A or B is trying to stop timer */
{
    pkt *mypktptr;
    struct event *evptr, *q;
    double lastime, x;
    int i;

    ntolayer3++;

    /* simulate losses: */
    if (mrand(1) < lossprob)
    {
        nlost++;
        if (TRACE > 0)
            printf("          TOLAYER3: packet being lost\n");
        return;
    }

    /* make a copy of the packet student just gave me since he/she may decide */
    /* to do something with the packet after we return back to him/her */
    mypktptr = (pkt *)malloc(sizeof(pkt));
    mypktptr->seqnum = packet.seqnum;
    mypktptr->acknum = packet.acknum;
    mypktptr->checksum = packet.checksum;
    /*wf: add support for sack */
    int j;
    for (j = 0; j < 5; j++){
        mypktptr->sack[j] = packet.sack[j];
    }
    /*wf: end */
    for (i = 0; i < 20; i++)
        mypktptr->payload[i] = packet.payload[i];
    if (TRACE > 2)
    {
        printf("          TOLAYER3: seq: %d, ack %d, check: %d ",
               mypktptr->seqnum, mypktptr->acknum, mypktptr->checksum);
    }

    /* create future event for arrival of packet at the other side */
    evptr = (struct event *)malloc(sizeof(struct event));
    evptr->evtype = FROM_LAYER3;      /* packet will pop out from layer3 */
    evptr->eventity = (AorB + 1) % 2; /* event occurs at other entity */
    evptr->pktptr = mypktptr;         /* save ptr to my copy of packet */
    /* finally, compute the arrival time of packet at the other end.
       medium can not reorder, so make sure packet arrives between 1 and 10
       time units after the latest arrival time of packets
       currently in the medium on their way to the destination */
    lastime = time_now;
    /* for (q=evlist; q!=NULL && q->next!=NULL; q = q->next) */
    for (q = evlist; q != NULL; q = q->next)
        if ((q->evtype == FROM_LAYER3 && q->eventity == evptr->eventity))
            lastime = q->evtime;
    evptr->evtime = lastime + 1 + 9 * mrand(2);

    /* simulate corruption: */
    /* modified by Chong Wang on Oct.21, 2005  */
    if (mrand(3) < corruptprob)
    {
        ncorrupt++;
        if ((x = mrand(4)) < 0.75)
            mypktptr->payload[0] = '?'; /* corrupt payload */
        else if (x < 0.875)
            mypktptr->seqnum = 999999;
        else
            mypktptr->acknum = 999999;
        if (TRACE > 0)
            printf("          TOLAYER3: packet being corrupted\n");
    }

    if (TRACE > 2)
        printf("          TOLAYER3: scheduling arrival on other side\n");
    insertevent(evptr);
}

void tolayer5(char datasent[])
{
    fwrite(datasent, 1, 20, fileoutput);
}