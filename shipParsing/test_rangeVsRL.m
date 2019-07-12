function [speedAtRMS,rangeAtRMS,rmsE,shipRange,timeAtRange,startTime]= test_rangeVsRL(wavData,textData,hdr,transitDateTime)

stIdx = 1;
edIdx = stIdx + 10e4;
idx1 = 1;
startTimeIdx = find(strcmp(textData.textdata(:,1),'UTC')==1)+1;
startTime = hdr.start.dnum;
timeAssoc = [];
rmsE = [];

while stIdx+10e4<=length(wavData)
    edIdx = stIdx + 10e4;
    timeAssoc(idx1,1) = startTime + ((idx1-1)*(10/(24*60*60)));
    rmsE(idx1) = 10*log10(sqrt(nanmean(wavData(stIdx:edIdx).^2)));
    stIdx = edIdx+1;
%     if timeAssoc(idx1,1)>=transitDateTime
%         break
%     end
    idx1 = idx1+1;
end

harpLatIdx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'HARPLat='))==1);
[k19,~]= regexp(textData.textdata{harpLatIdx,1},'HARPLat=(\d*\.\d*)','tokens','match');
HARPLat = str2double(k19{1,1});

harpLonIdx = find(~cellfun(@isempty,strfind((textData.textdata(:,1)),'HARPLon='))==1);
[k20,~]= regexp(textData.textdata{harpLonIdx,1},'HARPLon=(-\d*\.\d*)','tokens','match');
HARPLon = str2double(k20{1,1});

shipLat = textData.data(:,1);
shipLon = textData.data(:,2);

[x,y] = latlon2xy(shipLat,shipLon,HARPLat,HARPLon);
shipRange = (sqrt(x.^2+y.^2));
timeAtRange = datenum(textData.textdata(startTimeIdx:end,1));
speedAtTime = textData.data(:,4);

rangeAtRMS = zeros(size(timeAssoc));
speedAtRMS = zeros(size(timeAssoc));

for i2 = 1:length(timeAssoc)
    [minVal,minIdx] = min(abs(timeAssoc(i2)-timeAtRange));
    if minVal<(1/(24*60))
        rangeAtRMS(i2,1) = shipRange(minIdx);
        speedAtRMS(i2,1) = speedAtTime(minIdx);
    else
        rangeAtRMS(i2,1) = NaN;
        speedAtRMS(i2,1) = NaN;
    end
end
figure(23)
subplot(3,1,1)
plot(timeAssoc,rmsE)
datetick('x','keeplimits')
prevLims= get(gca,'xlim');
subplot(3,1,2)
plot(timeAtRange,shipRange,'*')
datetick('x')
set(gca,'xlim',prevLims)
subplot(3,1,3)
plot(rangeAtRMS,rmsE,'.')


%hold on