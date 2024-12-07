classdef arima_forecast < matlab.System
    % untitled Add summary here
    %
    % This template includes the minimum set of functions required
    % to define a System object.

    % Public, tunable properties
    properties
        n =10;
        p double =1;
        q double=1;
        D double =1;
    end

    % Pre-computed constants or internal states
    properties (Access = private)
        yold double;
        Mdl =arima(1,1,1);
          
    end

    methods (Access = protected)
        function setupImpl(obj)
            obj.yold = zeros(obj.n,1);
            obj.Mdl = arima(obj.p,obj.D,obj.q);
            % Perform one-time calculations, such as computing constants
        end

        function [y,t] = stepImpl(obj,ynew)
            % Implement algorithm. Calculate y as a function of input u and
            % internal states.
            %disp(obj.yold);
            %yold=obj.yold;
            x=zeros(obj.n,1);
            for i = 2:obj.n
                x(i-1)=obj.yold(i);
            end    
            x(obj.n)=ynew;
            EstMdl = estimate(obj.Mdl,x);
            y=forecast(EstMdl,obj.n,x);
            t=obj.n;
            obj.yold=x;
        end

        function resetImpl(obj)
            % Initialize / reset internal properties
        end

        function [sz_1,sz_2] = getOutputSizeImpl(obj) 
          sz_1 = [obj.n,1]; 
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

         function sts = getSampleTimeImpl(obj)
            sts = createSampleTime(obj,'Type','Discrete','SampleTime',1,'OffsetTime',0);
         end

    end
end
