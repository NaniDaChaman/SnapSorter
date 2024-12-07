classdef queue_sim < matlab.System
    % untitled Add summary here
    %
    % This template includes the minimum set of functions required
    % to define a System object.

    % Public, tunable properties
    properties
        time_horizon int32=10;%this will be the length of the input array
        n=5;
        res=0;
    end

    % Pre-computed constants or internal states
    properties (Access = private)
        queue double; %we want this to be a variable_length,2 array
        servers uint64;
        c int32=5;
        reset int32=0;
        old_queue=[[1,5],[1,7],[1,8]];
        old_servers=zeros(5,1);
    end

    methods (Access = protected)
        function setupImpl(obj)
            obj.c=obj.n;
            obj.reset=obj.res;
            %obj.old_queue=[[1,5],[1,7],[1,8]];
            %obj.old_servers=zeros(5,1);
            
            if obj.reset==0
                obj.old_servers=zeros(obj.c,1);
              obj.old_queue=zeros(0,2);
            obj.queue= zeros(0, 2);
            obj.servers=zeros(obj.c,1);
            end
            if obj.reset==1
                obj.queue=obj.old_queue;
                l=obj.old_servers;
                if l<obj.c
                    obj.old_servers=[obj.servers;zeros(obj.c-l,1)];
                else
                    obj.old_server=obj.servers(1:obj.c);
                end
                obj.servers=obj.old_servers;
            end
            %coder.varsize("obj.queue");
            % Perform one-time calculations, such as computing constants
        end

        function y=time_step(arrival,serving_time)
            temp=[];
            
            for i = 1:arrival
                temp=[temp;[0,serving_time]];
            end
            y=temp;
        end

        function [avg_response_time,queue_length] = stepImpl(obj,arrivals,serving_time,c)
            % Implement algorithm. Calculate y as a function of input u and
            % internal states.
            % our function will have two parts
            %the first part queues a bunch of arrivals in the queue
            j=1;%some kind of loop here 
            obj.c=c;
            %obj.servers=zeros(obj.c,1);
            if obj.reset==0
            obj.old_servers=zeros(obj.c,1);
              obj.old_queue=zeros(0,2);
            obj.queue= zeros(0, 2);
            obj.servers=zeros(obj.c,1);
            end
            if obj.reset==1
                obj.queue=obj.old_queue;
                l=length(obj.old_servers);
                if l<obj.c
                    obj.old_servers=zeros(obj.c,1);
                    obj.old_servers(1:l)=obj.old_servers;
                else
                    obj.old_servers=obj.servers(1:obj.c);
                end
                obj.servers=obj.old_servers;
            end
           % disp ('Start of new arrivals : ')
            %disp('State of our simulation :')
            %disp('Severs : ')
            %disp(obj.servers)
            %disp('Queues : ')
            %disp(obj.queue)
            response_time=[]
            while j <=obj.time_horizon
            %stores all the response times,avg it out in the end
            
            %disp(obj.servers)
            for i=(0:min(obj.servers))%servers might be zero
                %servers need to be -1 as it looks cooler
                %disp("State of the server");
                %disp(obj.servers);
                %disp("Value of j, where we are in the arrivals");
                %disp(j);
                %disp("Value of i, how much time is left to process the arrivals");
                %disp(i);
                temp=[]; 
                if j>obj.time_horizon
                    break; %in this case our obj.servers has not processed all the queues so
                    %the servers value and the queues value need to be
                    %carried over
                    obj.old_queue=obj.queue;
                    obj.old_servers=obj.servers;
                    obj.reset=1;
                end
                for k = 1:arrivals(j)
                    temp=[temp;[0,serving_time]]; 
                end
                %disp("first arrivals are : ")
                %disp(temp);
                if length(temp)>0
                l2=length(temp(:,1));
                l1=length(obj.queue(:,1));
                temp2=obj.queue;
                obj.queue=zeros(l2+l1,2);
                obj.queue(1:l1,:)=temp2;
                obj.queue(l1+1:end,:)=temp;
                end
                obj.queue(1:end,1)=obj.queue(1:end,1)+1; %increment the first row by 1
                j=j+1;   
            end
            
            obj.servers=obj.servers-min(obj.servers);%maybe we don't need them
            % the next part dequeus our stuff !!!
            while min(obj.servers)==0 && length(obj.queue)>0
                min_index=find(obj.servers==min(obj.servers(:)));
                min_index=min_index(1);
                %disp("server choosen : ")
                %disp(min_index);
                %disp("Object queue before_processing : ")
                %disp(obj.queue)
                if length(obj.queue)>0
                response_time=[response_time;sum(obj.queue(1,:))];
                st=obj.queue(1,2);
                %disp("Object queue after processing : ");
                
                obj.queue=obj.queue(2:end,:);
                %disp(obj.queue);
                obj.servers(min_index)=st;
                else
                    %response_time=[response_time;0];
                end  
            end
                %disp("Server times are");
                %disp(obj.servers);
                for k =(1:obj.c)
                    obj.servers(k)=max(obj.servers(k)-1,0);
                end
                %obj.servers=obj.servers-1;
                obj.queue(1:end,1)=obj.queue(1:end,1)+1;  
            
            end
            %disp("end of the simulation")
            %disp("Servers are : ")
            %disp(obj.servers)
            %disp("Queue is : ")
            %disp(obj.queue)
            if max(obj.servers)>0
                obj.reset=1;
                obj.old_queue=obj.queue;
                obj.old_servers=obj.servers;
            else
                obj.reset=0
            end
            avg_response_time = sum(response_time)/length(response_time);
            queue_length=length(obj.queue);
        end

        function resetImpl(obj)
            % Initialize / reset internal properties
        end
        function sts = getSampleTimeImpl(obj)
            sts = createSampleTime(obj,'Type','Discrete','SampleTime',1,'OffsetTime',0);
        end

        function [sz_1,sz_2] = getOutputSizeImpl(obj) 
          sz_1 = [1,1]; 
          sz_2 = [1 1]; 
          %sz_3=[obj.n,1]; 
        end

        function [out,out2] = getOutputDataTypeImpl(obj)
            % Return data type for each output port
            out = "double";
            out2 = "double";
            %out3="double";

            % Example: inherit data type from first input port
            % out = propagatedInputDataType(obj,1);
        end

        function [out,out2] = isOutputComplexImpl(obj)
            % Return true for each output port with complex data
            out = false;
            out2 = false;
            %out3=false;

            % Example: inherit complexity from first input port
            % out = propagatedInputComplexity(obj,1);
        end

        function [out,out2] = isOutputFixedSizeImpl(obj)
            % Return true for each output port with fixed size
            out = true;
            out2 = true;
            %out3=true;

            % Example: inherit fixed-size status from first input port
            % out = propagatedInputFixedSize(obj,1);
        end


    end
end
