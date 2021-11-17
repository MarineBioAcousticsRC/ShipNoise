function thisPassage = loadPassage(thisFile)

S = load(thisFile,'thisPassage');
thisPassage = (S.thisPassage(100:110,100:110)-50)/70;
end



%,thisCPA,thisDraught,round(thisHeading),...
    %round(thisLength),thisSOG,str2num(thisShipType),round(thisWidth)]';
% myData{2} = [round(thisCOG);
% myData{3} = thisCPA;
% myData{4} = thisDraught;
% myData{5} = round(thisHeading);
% myData{6} = round(thisLength);
% myData{7} = thisSOG;
% myData{8} = thisShipType;
% myData{9} = round(thisWidth)];
%myData{10} = thisDistVec;
%myData{3} = thisHmean;


