function plot_spectralmean(t, textData,hdr,specMat,fOrig)

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

%speedAtTime = textData.data(:,4);
startTimeIdx = find(strcmp(textData.textdata(:,1),'UTC')==1)+1;
timeAtRange = datenum(textData.textdata(startTimeIdx:end,1));
rangeAtT = [];
tDnum = (t/(60*60*24))+hdr.start.dnum;
for iT = 1:length(tDnum)
    [Tval,Tmin] = min(abs(tDnum(iT)-timeAtRange));
    if Tval<=(1/60*24)
    rangeAtT(iT,1) = shipRange(Tmin);
    else
        rangeAtT(iT,1) = NaN;
    end
end
figure(24)
plot(rangeAtT,mean(specMat(11:1001,:)),'*')



