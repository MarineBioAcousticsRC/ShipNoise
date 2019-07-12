
shipTypeAll = {};
IMOAll = [];
shipSizeAll = [];
draughtAll = [];
transitDateAll = [];
CPADistAll = [];
meanSOGAll = [];
fList = dir('J:\ShippingCINMS_data\*.mat');
nFiles = length(fList);
for iFile = 1:nFiles
    load(fullfile(fList(iFile).folder,fList(iFile).name),'shipType',...
        'IMO','shipSize','draught','meanSOG','CPADist','transitDate')
    shipType = cellfun(@char,shipType,'UniformOutput',0);

    shipTypeAll = [shipTypeAll;shipType];
    IMOAll = [IMOAll;IMO];
    shipSizeAll = [shipSizeAll;shipSize];
    draughtAll = [draughtAll;draught];
    transitDateAll = [transitDateAll;transitDate];
    CPADistAll = [CPADistAll;CPADist];
    meanSOGAll = [meanSOGAll;meanSOG];
end

shipTypeSet = {'Tug','Cargo','Passenger','Tanker','Other','Pleasure'};
shipTypeAll=strrep(shipTypeAll,'other','Other');
shipTypeAll=strrep(shipTypeAll,'30','Fishing');
shipTypeAll=strrep(shipTypeAll,'57','local');
shipTypeAll=strrep(shipTypeAll,'31','Tug');
shipTypeAll=strrep(shipTypeAll,'32','Tug');
shipTypeAll=strrep(shipTypeAll,'52','Tug');
shipTypeAll=strrep(shipTypeAll,'59','Special');
shipTypeAll=strrep(shipTypeAll,'35','Mil');
shipTypeAll=strrep(shipTypeAll,'37','Pleasure');
shipTypeAll=strrep(shipTypeAll,'70','Cargo');
shipTypeAll=strrep(shipTypeAll,'71','Cargo');
shipTypeAll=strrep(shipTypeAll,'72','Cargo');
shipTypeAll=strrep(shipTypeAll,'73','Cargo');
shipTypeAll=strrep(shipTypeAll,'74','Cargo');
shipTypeAll=strrep(shipTypeAll,'77','Cargo');
shipTypeAll=strrep(shipTypeAll,'79','Cargo');
shipTypeAll=strrep(shipTypeAll,'80','Tanker');
shipTypeAll=strrep(shipTypeAll,'81','Tanker');
shipTypeAll=strrep(shipTypeAll,'82','Tanker');
shipTypeAll=strrep(shipTypeAll,'83','Tanker');
shipTypeAll=strrep(shipTypeAll,'84','Tanker');
shipTypeAll=strrep(shipTypeAll,'89','Tanker');
shipTypeAll=strrep(shipTypeAll,'60','Passenger');
shipTypeAll=strrep(shipTypeAll,'69','Passenger');


shipTypeAllNum = nan(size(shipTypeAll));
for iType = 1:length(shipTypeSet)
    
    shipTypeAllNum(strcmp(shipTypeAll,shipTypeSet{iType}))= iType-1;
end


