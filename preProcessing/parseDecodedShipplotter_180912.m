function [ msg13_char, msg13_num, msg5_char, msg5_num ] = parseDecodedShipplotter_180912(aisFile)
% intended for use on decoded Shipplotter AIS files
% semicolon delimited
% stolen from parseDecodedSBARC_180814.m -> BJT
%
% need to figure out fields in Shipplotter files, using example string from coded
%
% Remaining fields depending on message ID? 
% https://www.navcen.uscg.gov/?pageName=AISMessages ) 
%
% We care about message ID:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   1-3 ( position report )  --> 11 fields
% 
%       Using example string from spnmea180511.txt:
%       $GPZDA,000040,11,05,2018,+00,00*69
%       !AIVDM,1,1,,A,15PLU6001IGIVNNCCMMrdpbj0<05,0*1A
%       
%       corresponding to line 1 in decoded file shipplotter180511.log:
%       369567000;under way ;000°'; 8.9kt;33.736305N;120.236455W;273.9°;277°;25s; 180511 000040;serial#1(A)[1]
%
%       decoded with http://www.maritec.co.za/tools/aisvdmvdodecoding/
%
%       field 1 = MMSI Number
%       field 2 = Navigational Status
%       field 3 = Rate of turn
%       field 4 = SOG
%       field 5 = Latitude
%       field 6 = Longitude 
%       field 7 = COG
%       field 8 = True Heading
%       field 9 = Time Stamp
%       field 10 = yymmdd HHMMSS
%       field 11 = receiver comms? (Class)[Message Type]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   5 ( Ship static/voyage data - manual input) --> 9 fields
%
%       Using example string from 2018-05-11 00:25:57
%       line 147 from spnmea180511.txt:
%
%       !AIVDM,2,1,2,A,55MU>f41pbaiLQ8r220l4PTl4PV222222222221643V@@5EWNHS1h`42AD`0p888,0*19

%       corresponding to line 76 shipplotter180511.log:
%       366563000;(7907996);(WHRN   );MAHIMAHI            ;Cargo ship ;-> May11 07:30 LGB PIER C          ;262 32 9.8 32 16; 180511 002557;serial#1(B)[5]
%       
%       decoded with http://www.maritec.co.za/tools/aisvdmvdodecoding/
%       
%       field 1 = MMSI Number
%       field 2 = IMO Number
%       field 3 = Call Sign
%       field 4 = Ship Name 
%       field 5 = Ship Type
%       field 6 = ETA MonthDay HH:MM Destination
%       field 7 = Ship dimensions: [a b c d e] 
%               a = to bow
%               b = to stern
%               c = draught
%               d = to port
%               e = to starbord
%               *example above decoded: A=32,B=230,C=16,D=16
%       field 8 = yymmdd HHMMSS
%       field 9 = receiver comms? (Class)[Message Type]
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   18 maybe ( position report for class B device )

% testing
% aisFile = 'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180718.txt';
% aisFile = 'D:\Projects\ShippingCINMS\code\matlab\AIS_SBARC_testFile.txt';

% date_fmt = 'yyyy-mm-dd HH:MM:SS:FFF';
date_fmt = 'yymmdd HHMMSS'; 

 fid = fopen(aisFile);
% looping over each line and growing cell array too slow...
% read in entire file using textscan, 
% should really ad in a check that textscan hasn't bombed before EOF...
rawData = textscan(fid,'%s','delimiter','\r\n');
fclose(fid);
rawData = rawData{1};
nFields = cellfun(@(x) length(find(x==';')),rawData)+1;
% find rows that contain the messages we care about
% message id 1-3
m13idx = find(nFields == 11);
% message id 5 
m5idx = find(nFields == 9);
 
% parse message id 1-3
m13Parts = regexp(rawData(m13idx),';','split');
n13 = length(m13Parts);
msg13_num = nan(n13,8); % dnum, MMSI, navStatus, SOG, lon, lat, COG, true heading
msg13_char = cell(n13,1); % ship name
% tic
msgId = nan(n13,1);
for mi = 1:n13
%     if mod(mi,5e3) == 0
%         fprintf('\tmsg %d/%d\n', mi,n13);
%     end
    msg13 = m13Parts{mi};

%     msg13_char{mi,1} = msg13{3};
    msg13_char{mi,1} = 'unknown'; % ship name not in Shipplotter Message types 1,2,3
    
%     dnum = datenum(sprintf('%s %s', msg13{1}, msg13{2}),date_fmt);
    dnum = datenum(msg13{10},date_fmt);
    MMSI = str2double(msg13{1});
%     navStatus = str2double(msg13{2});
    navStatus = 0;  % force to be 'under way' status since field is text
    SOG = str2double(msg13{4}(1:end-2)); % remove 'kt'
    lon = -str2double(msg13{6}(1:end-1)); % remove letter 'W' and make negative
    lat = str2double(msg13{5}(1:end-1)); % remove letter 'N'
    COG = str2double(msg13{7}(1:end-1)); % remove degree symbol
    trueHeading = str2double(msg13{8}(1:end-1)); % remove degree symbol
    
    msg13_num(mi,:) = [ dnum, MMSI, navStatus, SOG, lon, lat, COG, trueHeading ];
    
    a = regexp(msg13{11},'[');
    b = regexp(msg13{11},']');
    msgId(mi) = str2double(msg13{11}(a+1:b-1)); % need to parse out [x] value
end
% toc

clear m13Parts; % this variable gets huge

% make sure we only have good messages, some have message ID in wrong spot?
badMsg13 = find(~ismember(msgId,[1,2,3]));
msg13_num(badMsg13,:) = [];
msg13_char(badMsg13) = [];
fprintf('\tRemoved %d bad position messages\n',length(badMsg13));

% parse message id 5
m5Parts = regexp(rawData(m5idx),';','split');
n5 = length(m5Parts);
msg5_num = nan(n5,8); % UTC datenum, MMSI, IMO, draught [m], ship type, toBow, toStern, toPort, toStarboard
msg5_char = cell(n5,2); % ship name, ship type
% tic
for mi = 1:n5
%     if mod(mi,5e3) == 0
%         fprintf('\tmsg %d/%d\n', mi,n5);
%     end
    msg5 = m5Parts{mi};
    
    shipName = msg5{4};
    shipType = msg5{5};
  
    msg5_char{mi,1} = shipName;
    msg5_char{mi,2} = shipType;
    
    dnum = datenum(msg5{8},date_fmt);   
    MMSI = str2double(msg5{1});
    
    a = regexp(msg5{2},'(');
    b = regexp(msg5{2},')');
    IMO = str2double(msg5{2}(a+1:b-1)); 
    
    f7 = regexp(msg5{7},' ','split');
    draught = str2double(f7{3});    
    toBow = str2double(f7{1});
    toStern = str2double(f7{2});
    toPort = str2double(f7{4});
    toStarboard = str2double(f7{5});
    msg5_num(mi,:) = [ dnum, MMSI, IMO, draught, toBow, toStern, toPort, toStarboard ];
end
% toc
clear m5Parts
1;

