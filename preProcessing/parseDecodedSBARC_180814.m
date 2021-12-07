function [ msg13_char, msg13_num, msg5_char, msg5_num ] = parseDecodedSBARC_180814(aisFile)
% intended for use on decoded SBARC AIS files
% semicolon delimited
% need to figure out fields in SBARC files, using example string from coded

%
% Remaining fields depending on message ID? 
% https://www.navcen.uscg.gov/?pageName=AISMessages ) 
%
% We care about message ID:
%   1-3 ( position report )  --> 21 fields
% 
%       Using example string from 2018-07-18;00:00:06.825
%       !AIVDM,1,1,,A,35NRKePPBWoM2KhCQ5k1tQ3j00d@,0*11
%       
%       should correspond to line 14 in decoded file:
%       2018-07-18;00:00:06:759;ISLAND EXPLORER;3;0;367565750;0;129;16.7;1;-119.485833;34.108500;49.8;33;56;0;0;0;0;286;0
%
%       decoded with http://www.maritec.co.za/tools/aisvdmvdodecoding/
%
%       field 1 = UTC date
%       field 2 = UTC time
%       field 3 = Ship Name
%       field 4 = message ID
%       field 5 = repeat indicator?
%       field 6 = MMSI number 
%       field 7 = navigational status?
%       field 8 = Rate of turn
%       field 9 = SOG [ knots ]
%       field 10 = Position accuracy
%       field 11 = lon
%       field 12 = lat 
%       field 13 = COG ( 1/10 )
%       field 14 = true heading
%       field 15 = UTC second of report
%       field 16 = Special manoeuvre indicator?
%       field 17 = ?
%       field 18 = ?
%       field 19 = ?
%       field 20 = slot increment 
%       field 21 = ?

%   5 ( static/voyage data ) --> 19 fields
%       Using example strings from 2018-07-18;00:00:28:386

%       !AIVDM,2,1,7,B,58154M02=nHIKL`sJ21T5<61DpUAV22222222216H`LF:5q6NAUDp33Qp0Q@,0*71
%       !AIVDM,2,2,7,B,@j888888880,2*0A
%       
%       decoded with http://www.maritec.co.za/tools/aisvdmvdodecoding/
%       ...still not sure which field is draught in decoded data
%       
%       appears to correspond with line 65
%       2018-07-18;00:00:28:386;5;0;538002548;0;9296262;V7JN6;YASA UNITY;70;197;28;22;10;1;496030;70;US LNG BEACH;0
%       field 1 = UTC date
%       field 2 = UTC time
%       field 3 = message ID
%       field 4 = repeat indicator? 
%       field 5 = MMSI number
%       field 6 = ?
%       field 7 = IMO number
%       field 8 = call sign
%       field 9 = ship name
%       field 10 = ship type/cargo? 
%           https://www.navcen.uscg.gov/?pageName=AISMessagesAStatic#TypeOfShip
%       field 11 = to bow [m]
%       field 12 = to stern [m]
%       field 13 = to port [m]
%       field 14 = to starboard [m]
%       field 15 = EPFD?
%       field 16 = 
%       field 17 = static draught? [ in 1/10 m ] 
%       field 18 = destination
%       field 19 = ?
%
%
%   18 maybe ( position report for class B device )

% testing
% aisFile = 'D:\Projects\ShippingCINMS\AIS\SBARC\AIS_SBARC_180718.txt';
% aisFile = 'D:\Projects\ShippingCINMS\code\matlab\AIS_SBARC_testFile.txt';

date_fmt = 'yyyy-mm-dd HH:MM:SS:FFF';

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
m13idx = find(nFields == 21);
% message id 5 
m5idx = find(nFields == 19);
 
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

    msg13_char{mi,1} = msg13{3};
    
    dnum = datenum(sprintf('%s %s', msg13{1}, msg13{2}),date_fmt);
    MMSI = str2double(msg13{6});
    navStatus = str2double(msg13{7});
    SOG = str2double(msg13{9});
    lon = str2double(msg13{11});
    lat = str2double(msg13{12});
    COG = str2double(msg13{13});
    trueHeading = str2double(msg13{14});
    
    msg13_num(mi,:) = [ dnum, MMSI, navStatus, SOG, lon, lat, COG, trueHeading ];
    
    msgId(mi) = str2double(msg13{4});
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
    
    shipName = msg5{9};
    shipType = msg5{10};
  
    msg5_char{mi,1} = shipName;
    msg5_char{mi,2} = shipType;
    
    dnum = datenum(sprintf('%s %s', msg5{1}, msg5{2}),date_fmt);   
    MMSI = str2double(msg5{5});
    IMO = str2double(msg5{7});    
    draught = str2double(msg5{17})/10;    
    toBow = str2double(msg5{11});
    toStern = str2double(msg5{12});
    toPort = str2double(msg5{13});
    toStarboard = str2double(msg5{14});
    msg5_num(mi,:) = [ dnum, MMSI, IMO, draught, toBow, toStern, toPort, toStarboard ];
end
% toc
clear m5Parts


1;
% 
% 
% tline = fgetl(fid);
% lc = 1;
% tic
% while ~feof(fid)
%     lparts = regexp(tline,';','split');
%     if mod(lc,10e3) == 0
%         toc
%         fprintf('\tLine %d\n', lc);
%         tic
%     end
%     if length(lparts) == 21 && ismember(str2double(lparts{4}),[1,2,3]) % message 1-3
%         dnum = datenum(sprintf('%s %s', lparts{1}, lparts{2}),date_fmt);
%         shipName = lparts{3};
%         MMSI = str2double(lparts{6});
%         navStatus = lparts{7};
%         SOG = str2double(lparts{10});
%         lon = str2double(lparts{11});
%         lat = str2double(lparts{12});
%         COG = str2double(lparts{13});
%         trueHeading = str2double(lparts{14});    
%         msg13 = vertcat(msg13, { dnum, shipName, MMSI, navStatus, SOG, lon, lat, COG, trueHeading });
%         1;
%     elseif length(lparts) == 19 && str2double(lparts{3}) == 5
%         dnum = datenum(sprintf('%s %s', lparts{1}, lparts{2}),date_fmt);
%         shipName = lparts{9};
%         MMSI = str2double(lparts{5});
%         IMO = str2double(lparts{7}); 
%         shipType = lparts{10}; 
%         toBow = lparts{11};
%         toStern = lparts{12};
%         toPort = lparts{13};
%         toStarboard = lparts{14};
%         draught = str2double(lparts{17})/10;
%         msg5 = vertcat(msg5, { dnum, shipName, MMSI, IMO, shipType, toBow, toStern, toPort, toStarboard, draught });
%         1;
%     end
% %     if length(lparts)~=21
% %     if length(lparts)<21
% %       if length(lparts)==23
% %       if length(lparts)==21
% %         fprintf('%d = %d parts\n', lc, length(lparts));
% %         fprintf('\t%s\n', tline);
% %         fprintf('line %d\tsize %d\t%s\n', lc,length(lparts),lparts{4});
%     nparts(lc) = length(lparts);
%     tline = fgetl(fid);
%     lc=lc+1; 
% end
% 
% fclose(fid);
%  
%  toc
%  
% 1;
% 

