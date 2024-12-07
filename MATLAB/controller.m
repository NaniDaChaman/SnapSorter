function [avg_response_time,queue_length] = controller(time_horizon,arrivals,serving_time,c)
%#codegen
persistent queue servers reset old_c r old_queue old_servers
coder.varsize("old_queue", [1000, 2], [true,false])
coder.varsize("queue", [1000, 2], [true,false])

% our function will have two parts
%the first part queues a bunch of arrivals in the queue
j=1;%some kind of loop here 
old_c=c;
reset=0;
%if reset ==0
    old_servers=zeros(old_c,1);
    old_queue=zeros(1,2);
    queue= zeros(1, 2);
    servers=zeros(old_c,1);
%end
%if reset==1
    %queue=old_queue;
    %l=length(old_servers);
    %if l<old_c
        %old_servers=zeros(old_c,1);
        %old_servers(1:l)=old_servers;
    %else
        %old_servers=servers(1:old_c);
    %end
   % servers=old_servers;
%end

%disp ('Start of new arrivals : ')
%disp('State of our simulation :')
%disp('Severs : ')
%disp(servers)
%disp('Queues : ')
%disp(queue)
coder.varsize("response_time", [1000, 1], [true,false])
response_time=[]

while j <=time_horizon
%stores all the response times,avg it out in the end
for i=(0:min(servers))%servers might be zero
    %servers need to be -1 as it looks cooler
    %disp("State of the server");
    %disp(servers);
    %disp("Value of j, where we are in the arrivals");
    %disp(j);
    %disp("Value of i, how much time is left to process the arrivals");
    %disp(i);
    temp=[]; 
    if j>time_horizon
        break; %in this case our obj.servers has not processed all the queues so
        %the servers value and the queues value need to be
        %carried over
        old_queue=queue;
        old_servers=servers;
        reset=1;
    end
    for k = 1:arrivals(j)
        temp=[temp;[0,serving_time]]; 
    end
    %disp("first arrivals are : ")
    %disp(temp);
    if length(temp)>0
    l2=length(temp(:,1));
    l1=length(queue(:,1));
    temp2=queue;
    queue=zeros(l2+l1,2);
    queue(1:l1,:)=temp2;
    queue(l1+1:end,:)=temp;
    end
    queue(1:end,1)=queue(1:end,1)+1; %increment the first row by 1
    j=j+1;   
end

servers=servers-min(servers);%maybe we don't need them
% the next part dequeus our stuff !!!
while min(servers)==0 && length(queue)>0
    min_index=find(servers==min(servers(:)));
    min_index=min_index(1);
    %disp("server choosen : ")
    %disp(min_index);
    %disp("Object queue before_processing : ")
    %disp(queue)
    if length(queue)>0
    response_time=[response_time;sum(queue(1,:))];
    st=queue(1,2);
    %disp("Object queue after processing : ");
    
    queue=queue(2:end,:);
    %disp(queue);
    servers(min_index)=st;
    else
        %response_time=[response_time;0];
    end  
end
%disp("Server times are");
%disp(servers);
for k =(1:c)
    servers(k)=max(servers(k)-1,0);
end
%obj.servers=obj.servers-1;
queue(1:end,1)=queue(1:end,1)+1;  

end
%disp("end of the simulation")
%disp("Servers are : ")
%disp(servers)
%disp("Queue is : ")
%disp(queue)
if max(servers)>0
reset=1;
old_queue=queue;
old_servers=servers;
else
reset=0
end
avg_response_time = sum(response_time)/length(response_time);
queue_length=length(queue);


%x=sum(x);
%y=x;
end