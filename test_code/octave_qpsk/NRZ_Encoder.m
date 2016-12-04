% NRZ_Encoder Line codes encoder
% [time,output,Fs]=NRZ_Encoder(data,Rb,amplitude,style)
% NRZ_Encoder NRZ encoder
% data a stream of bits and specify bit-Rate, amplitude of the output signal and the style of encoding
% Currently 3 encoding styles are supported namely 'Manchester','Unipolar'and 'Polar'
% Outputs the NRZ stream

function [time,output,Fs]=NRZ_Encoder(data,Rb,amplitude,style)
  Fs=10*Rb; %Sampling frequency , oversampling factor= 32
  Ts=1/Fs; % Sampling Period
  Tb=1/Rb; % Bit periodoutput=[];
  output=[];
  a = 1;

  switch lower(style)
    case {'manchester'}
    for count=1:length(data),
      for tempTime=0:Ts:Tb/2-Ts,
        output=[output (-1)^(data(count))*amplitude];
      end

      for tempTime=Tb/2:Ts:Tb-Ts,
        output=[output (-1)^(data(count)+1)*amplitude];
      end
    end

    case {'unipolar'}
    for count=1:length(data),
      for tempTime=0:Ts:Tb-Ts,
        output=[output data(count)*amplitude];
      end
    end

    case {'polar'}
      for count=1:length(data),
        for tempTime=0:Ts:Tb-Ts,
          output(a)=[amplitude*(-1)^(1+data(count))];
          a++;
      end
    end

    otherwise,
    disp('NRZ_Encoder(data,Rb,amplitude,style)-Unknown method given as ''style'' argument');
    disp('Accepted Styles are ''Manchester'', ''Unipolar'' and ''Polar''');
  end

  time=0:Ts:Tb*length(data)-Ts;
