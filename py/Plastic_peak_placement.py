import numpy as np
import os

###############################################################
###                   User Settings                         ###
###############################################################
# blackout_first=True #from epi layer
gamma=True #else electrons
jobtime="13:00:00"
jobtime_hadd="5:00:00"

###############################################################
### Run different settings depending on computer or cluster ###
###############################################################
nodename=os.uname().nodename

# nodename="bp1-login01.data.bp.acrc.priv"

if nodename=="it034449.users.bris.ac.uk":
	materials_path="/Users/lb8075/gate-exercices-master-linac/linac/data/GateMaterials.db"	
	if gamma:
		phasespace_in="/Users/lb8075/gate-exercices-master-linac/linac/generatedGammasnSkimmed10Halfmm1.root"
	else:
		phasespace_in="/Users/lb8075/gate-exercices-master-linac/linac/output-lana2-PhS-e_500g4x3.root"
	file_number='1'
	how_many_primaries=200
	out_dir="/Users/lb8075/gate-exercices-master-linac/linac/output/"
	mac_loc="/Users/lb8075/gate-exercices-master-linac/linac/mac/"
	seed_rand=12345678
elif nodename=="bp1-login01.data.bp.acrc.priv":
	materials_path="/home/lb8075/linac/data/GateMaterials.db"
	if gamma:
		phasespace_in="/work/lb8075/PhaseSpaces/PhS2Gamma/output-lana2-PhS-g_nobias{id}.root"
	else:
		phasespace_in="/work/lb8075/PhaseSpaces/PhS2Elec/output-lana2-PhS-e_nobias{id}.root"
	file_number="$PBS_ARRAY_INDEX"
	how_many_primaries="${Nparts[$PBS_ARRAY_INDEX-1]}"
	out_dir="/work/lb8075/PhaseSpaces/Flex/"
	mac_loc="/home/lb8075/linac/mac/"
	seed_rand="$RANDOM$RANDOM$RANDOM"
else:
	raise ValueError('Nodename not recognised')

###############################################################
###       Set up dimensions, materials, translations        ###
###############################################################

grating_thicknesses=np.array([30,50,80,100,300]) #um 30,50,80,100,200,300,350,400,500
BlackOut_distances=np.array([0,10]) #mm
BlackOut_thickness=np.array([20,100,300]) #um 100,200,300,500,1000
blackout_material=np.array(['Polyethylene','Silicon','Aluminium'])
peak_material=np.array(['Lead','Silicon','Aluminium'])

front_face_epi_mm=450 #mm
front_face_epi_um=front_face_epi_mm*1000 #um

translation_BO_um=0
translation_peak_um=0

# distance_BlackOut_to_peaks_mm=10 #mm

####### BlackOut distance from surface?!!

###############################################################
###        Create start of pbs submission file              ###
###############################################################

macrofile=f"{mac_loc}Main_PhS3_10x10_Flexible.mac"
hadd_string=f"#!/bin/bash \n\
#PBS -l walltime={jobtime_hadd} \n\
#PBS -j oe\n\
#PBS -l select=1:ncpus=1\n\
#PBS -l select=1:ncpus=1:mem=500mb\n\
#PBS -o /work/lb8075/job_logfiles\n\
\n\
module add apps/gate/8.2\n"

pbs_string=f"#!/bin/bash \n\
#PBS -l walltime={jobtime} \n\
#PBS -j oe\n\
#PBS -l select=1:ncpus=1\n\
#PBS -l select=1:ncpus=1:mem=500mb\n\
#PBS -J 1-988\n\
#PBS -o /work/lb8075/job_logfiles\n\
\n\
module add apps/gate/8.2\n"
if gamma:
	pbs_string+="Nparts=(12324799 12344333 12320787 12358361 12351653 12343871 12348580 12377844 12359044 12359558 12339245 12348723 12390508 12378512 12381074 12340780\
12359019 12380818 12310263 12371441 12374875 12325019 12344434 12331759 12378988 12351222 12403313 12335501 12364976 12356855 12388273 12346750 12359575 12334015 12358989\
12358076 12348926 12347520 12362180 12358310 12365191 12352399 12357959 12359978 12317036 12354435 12318754 12366124 12359250 12315165 12345842 12317852 12349948 12325936\
12351486 12356296 12360431 12314638 12396307 12357984 12354090 12356510 12354666 12359407 12363992 12315285 12385841 12335594 12337404 12368744 12376725 12359634 12358969\
12342484 12327755 12375507 12325143 12332087 12373730 12359673 12364984 12349303 12350554 12360487 12360180 12339307 12345321 12323445 12378407 12367684 12321469 12365717\
12331399 12395137 12357078 12339263 12342306 12330403 12359089 12340791 12326845 12347218 12354933 12344015 12346601 12354179 12346934 12355713 12381516 12366222 12343916 12357779\
12395367 12359966 12373757 12364336 12372037 12343944 12325341 12330704 12368418 12351294 12373448 12354457 12367227 12363213 12340773 12359629 12312717 12349045 12359260 12350077\
12358201 12349851 12346356 12327767 12348651 12357457 12365848 12350719 12336411 12340953 12371287 12368972 12345267 12329875 12364720 12360855 12343445 12316769 12374257 12375278\
12333572 12347105 12359519 12344835 12362815 12332340 12379206 12377311 12340673 12369305 12376664 12386068 12339697 12359025 12365183 12320606 12372068 12340510 12358013 12347548\
12323893 12348604 12335304 12359128 12386992 12357313 12386393 12366891 12340845 12341816 12352096 12379991 12359622 12354759 12385894 12362212 12348939 12337470 12373215 12348443\
12357541 12337796 12356805 12403346 12353639 12324316 12342328 12339408 12326261 12342619 12300141 12370160 12337221 12358683 12367096 12400738 12353538 12344487 12351744 12353299\
12366720 12378891 12347131 12357571 12358184 12346931 12347577 12344580 12374176 12363520 12339026 12361504 12363280 12348604 12340160 12357366 12328090 12360804 12348001 12368803\
12343077 12374158 12341027 12347719 12362948 12353570 12341804 12354273 12377340 12370168 12354897 12346409 12339332 12363332 12360277 12322592 12303434 12371186 12354146 12367591\
12348259 12350596 12347488 12375658 12347652 12361088 12357944 12337385 12338444 12355883 12364704 12343429 12376278 12360028 12378964 12372637 12348772 12346442 12358126 12381434\
12374707 12329131 12351050 12345170 12380162 12379611 12352386 12357648 12368495 12382107 12354943 12339997 12387672 12378588 12359415 12337963 12358109 12330936 12395777 12345154\
12341961 12338718 12369765 12375319 12343775 12346147 12368642 12339727 12334664 12374600 12333286 12357410 12361195 12358135 12331621 12340309 12355890 12334910 12341934 12337980\
12359982 12322772 12369119 12371479 12352034 12312830 12376609 12352042 12329863 12348997 12371960 12337680 12367770 12343313 12374129 12372279 12385633 12388204 12352809 12350768\
12353970 12332169 12341679 12350204 12372410 12372076 12305473 12356162 12369447 12356457 12333308 12372017 12367804 12357723 12360122 12369525 12364414 12360515 12342094 12356788\
12348567 12361168 12369619 12353444 12367460 12357449 12356458 12329057 12321151 12326645 12374847 12377488 12340370 12326726 12355784 12377259 12379382 12305858 12348657 12345033\
12367955 12341178 12321000 12358532 12359820 12362280 12374639 12329195 12345583 12354223 12377900 12346759 12392752 12350849 12340132 12350135 12352565 12380307 12381645 12347512\
12345074 12377777 12387687 12356305 12370160 12344398 12367688 12354603 12356622 12376008 12369114 12350615 12357775 12335494 12330205 12335195 12322311 12353673 12351993 12371721\
12323217 12369062 12375649 12359918 12345619 12343028 12313443 12315102 12357717 12347171 12372256 12384832 12356308 12340613 12382730 12340878 12345290 12389370 12355613 12375250\
12347365 12331977 12366622 12314413 12330451 12345672 12337084 12363407 12367851 12366832 12331710 12349689 12378513 12343753 12375112 12360496 12306178 12363950 12355667 12365287\
12314701 12328518 12340034 12351288 12350140 12355861 12387262 12340931 12362292 12353417 12355127 12345554 12357967 12338164 12358148 12372799 12383772 12359297 12334593 12374045\
12359417 12366132 12359143 12310138 12357024 12339849 12359358 12352536 12338349 12359887 12385809 12330744 12387629 12340302 12381836 12359175 12329892 12337374 12361926 12350376\
12326795 12327659 12369385 12372214 12348293 12382536 12344918 12364523 12357854 12340184 12378226 12306920 12359912 12344782 12340429 12381974 12358352 12361551 12357221 12355889\
12301239 12349026 12383904 12349264 12331672 12347766 12370274 12369317 12366971 12338186 12376657 12385191 12359196 12352957 12374144 12327478 12363243 12379600 12364561 12358888\
12373487 12355411 12331679 12337673 12349618 12385128 12370920 12348800 12326037 12355645 12377348 12365449 12364736 12347785 12374714 12352559 12339278 12366046 12339597 12365769\
12359747 12382367 12358576 12383599 12362690 12379148 12370028 12350920 12352648 12366765 12361570 12347983 12358482 12342991 12374254 12345454 12371594 12390540 12338499 12315394\
12371706 12337326 12341813 12352324 12345648 12380944 12351403 12333022 12359108 12375008 12379337 12344925 12357437 12319623 12358919 12352840 12371262 12335959 12357198 12371532\
12360508 12332739 12346969 12341014 12335203 12391090 12337008 12379869 12338376 12369808 12359563 12359556 12367670 12355247 12372785 12358760 12357507 12357952 12371474 12343531\
12317431 12373229 12375739 12345390 12351085 12345108 12363701 12354196 12359418 12382001 12349825 12321375 12366309 12358988 12338082 12375503 12388587 12355402 12337146 12386620\
12375289 12358418 12377579 12347270 12366561 12349151 12364851 12367210 12324066 12374560 12338508 12339977 12364912 12361290 12363519 12374067 12382692 12350224 12331918 12381332\
12380413 12358213 12361861 12344635 12371886 12334874 12365949 12349334 12348934 12386121 12392656 12363136 12357785 12335456 12353637 12313970 12335579 12366110 12369225 12348568\
12344659 12326971 12359920 12358684 12374272 12362029 12338352 12387347 12358587 12385132 12346821 12347190 12348279 12358929 12398662 12356297 12319750 12364764 12332911 12363213\
12344721 12357713 12348309 12366131 12362873 12349732 12350894 12361203 12343641 12359649 12329443 12317555 12343744 12343490 12373611 12350263 12341260 12347528 12370246 12368177\
12363608 12365019 12369467 12322311 12361820 12361535 12352574 12346058 12381610 12350713 12334017 12360947 12357046 12354054 12387670 12355621 12372292 12365305 12351411 12341120\
12359166 12357695 12355730 12342102 12345247 12372314 12355715 12363657 12338300 12361629 12330044 12377357 12368230 12351655 12363432 12360154 12366794 12367312 12372369 12351902\
12359192 12328428 12330010 12337810 12316738 12323916 12331924 12323239 12392508 12352420 12392651 12367149 12342990 12367752 12363862 12330165 12354516 12342849 12346777 12397522\
12321808 12336759 12376049 12355263 12381487 12353464 12327432 12361870 12330170 12342435 12381772 12329993 12405384 12381396 12350431 12359421 12336092 12359010 12367363 12358681\
12334828 12347922 12389870 12351251 12364035 12326783 12358533 12357277 12348658 12335094 12346501 12359162 12360572 12342889 12376179 12383411 12344352 12353134 12308830 12342801\
12362689 12342441 12365264 12388376 12368754 12356216 12332847 12349780 12370614 12321713 12341448 12354436 12384296 12355530 12358632 12342754 12357102 12391463 12381308 12339114\
12378635 12307678 12385773 12356722 12369115 12359028 12338707 12338123 12370191 12357360 12335664 12306950 12379314 12318121 12365828 12359697 12360049 12342722 12336134 12320913\
12322685 12349870 12350577 12362208 12331963 12346240 12333461 12333986 12331311 12359986 12362293 12349954 12339589 12359281 12341840 12336353 12350850 12361492 12327705 12358709\
12342123 12368003 12356560 12360449 12363750 12357615 12382228 12356655 12344706 12356878 12369821 12346120 12379049 12341471 12371707 12371122 12354160 12390148 12384695 12362502\
12317224 12346722 12373507 12337770 12353848 12385450 12351025 12359875 12351268 12360571 12358031 12358604 12356643 12363005 12345796 12391633 12389778 12323961 12354799 12341076\
12356114 12360274 12340633 12357085 12358944 12313055 12364061 12386904 12348493 12343857 12343146 12371609 12365106 12355421 12352160 12352651 12352182 12330718 12356229 12371025\
12346415 12338653 12360766 12365128 12434357 12368720 12360477 12355016 12367541 12389527 12334772 12365917 12358770 12346229 12356365 12318195 12319097 12334980 12359127 12352678\
12344376 12333287 12356703 12356650 12360067 12340790 12329024 12356539 12351012 12362051 12351203 12370041 12372130 12355968 12314682 12332723 12351443 12380373 12387019 12352316\
12354111 12357216 12349765 12338583 12366914 12348176 12363603 12348538 12362237 12347638 12388291 12358954 12341697 12303298)\n"
else:
	pbs_string+="Nparts=(723076 726689 721588 723309 721878 724607 724267 724281 727185 726609 726190 726936 722418 723290 724835 727439 729605 724112 728417 727185 \
724309 722563 726427 725083 724069 723800 723569 724427 724106 724285 726967 724286 725382 724372 725303 721256 725093 726255 726582 725262 725861 725578 725627 724605\
725335 721732 724895 724857 725169 723918 723629 723852 723977 721671 723817 722571 726982 725637 725456 722179 729600 725144 726037 725565 724249 725913 725478 723888\
727054 724376 724045 724665 723205 725440 726709 722246 723684 724543 722874 725219 725054 727738 724196 725892 725027 725946 726214 725221 724601 724853 724660 725109\
723747 726553 722942 729880 726564 724176 725524 723464 726473 723354 723819 724795 726651 725743 724592 724810 722586 723189 723637 722944 726234 724773 727433 726050\
727257 725847 722684 721459 723612 724387 723968 723302 726953 728120 724587 727705 722730 725946 725465 721650 724488 724482 725371 724987 724165 726479 723214 726140\
726760 724883 725704 724611 723897 726129 721605 722726 724646 722547 721644 725835 723433 726584 723170 722628 725836 724803 724918 725127 727987 726074 724729 726055\
725774 725340 724625 723951 728024 724103 723363 723708 726447 724672 722414 725876 719671 724013 725690 725236 728701 723135 723564 724516 725365 726420 725174 722192\
725026 724963 726450 722928 724875 726054 726089 723149 723545 726449 724016 723395 725411 724315 723936 722153 721599 726113 724167 725625 724845 726694 721967 724921\
725513 724924 726978 727700 724100 725372 725449 723254 722670 724542 725674 723996 723895 728696 725272 726265 723808 725377 723132 725151 724409 725686 724260 724487\
724705 724652 726233 722340 724254 724545 724568 727878 724491 725650 723508 726329 726237 724508 724998 724148 726590 723836 724987 725977 725445 723631 722033 722647\
727058 724104 722650 723677 726998 724300 725349 723327 721956 727520 723390 722548 726163 725821 724856 725087 723563 724379 726348 725662 725027 726247 725448\
726384 724260 724789 726576 724763 725133 723284 726155 726735 725811 722242 725431 725280 727713 723809 726035 723293 725818 726355 722930 723314 725495 726366\
724089 724434 723503 725759 725055 725755 721770 724691 724866 721309 726068 724279 722410 723021 724789 726469 723750 724356 725220 723465 725121 726949 725243\
727030 727271 724328 723908 723070 723576 726984 722429 725535 727656 724998 723280 726084 723724 724438 724229 729832 724171 723970 725830 722564 725790 723994\
725003 725776 724562 724964 723843 723024 726605 724180 723544 724910 724183 727454 726564 726083 724297 722782 723934 722827 724798 722496 725908 725968 726157\
724446 726784 725866 725659 725301 724830 723795 725016 725182 724509 728222 728463 725547 724404 726553 726647 726892 725749 726019 725257 726135 724712 724265\
726075 725502 726078 723472 723119 723671 726116 722487 724612 725813 723731 722530 723409 723850 725363 726688 726058 724644 722291 726379 723202 726349 722923\
721601 725054 726895 724477 726129 724403 724982 727009 726136 726046 726862 722656 725467 725559 724410 728114 723273 721308 722380 725032 727881 725583 723893\
723954 724265 722794 724472 726254 723853 723678 725097 723135 726586 723020 725454 723345 724867 725501 725197 727693 723504 727448 720733 724368 723821 725894\
725116 724927 724770 726739 724595 723575 727506 724034 726855 726251 723215 725749 722302 726331 726058 724485 721575 726030 723343 728725 724329 725925 725959\
722761 724936 726470 724095 722764 721677 723201 724458 726320 725528 726434 726902 725303 726964 722379 724837 726761 722830 727971 728213 727170 724044 725937\
725111 720642 721158 723834 724772 723659 725883 722030 723087 724606 724132 725024 724812 726720 724710 725991 724084 723966 723364 724312 725194 725049 727681\
724498 723832 723000 726156 724486 725614 723740 724594 725502 726844 725409 724703 724997 724691 724524 724902 725458 724090 725399 723077 723794 723970\
725237 725337 725216 724703 726366 725209 726236 724565 723816 720377 725083 724954 727509 724640 724809 725176 723952 721929 724732 725952 725042 726936\
721760 724380 725815 724355 723514 726895 726936 723954 725937 725184 723922 726372 724006 726794 723884 722592 723631 723310 726535 729005 721193 726778\
723038 726178 725729 725612 726028 727376 724539 721571 723273 723068 727239 724139 722642 727298 726647 723862 724215 720096 725408 721976 722728 724811\
723214 724874 725646 725973 725350 728053 727531 725635 722744 724688 724986 725375 723303 724405 723845 721408 726287 728747 724555 723782 722168 725824\
724662 723397 726653 726518 724925 726616 722157 727076 725238 725637 723491 723200 723198 723801 722995 723598 727194 726385 723671 723380 724405 724636\
724253 723616 725540 722253 723611 724800 724812 723328 726779 723398 722544 722776 723949 727821 722561 725153 724936 725671 724240 724957 725454 725689\
725074 727249 722985 722606 724318 726204 723272 723876 725941 725346 725427 726196 724201 723423 720398 723084 727432 725667 727891 729006 726788 721930\
727330 725223 725845 724978 722502 723552 727705 721580 722182 726215 725244 724578 722989 723674 720846 725392 724938 724126 725479 725296 728237 724193\
723820 724813 725593 723551 723518 727767 726731 725526 724382 725413 720867 725396 722725 724561 728035 725049 723250 725518 725715 721646 726531 721807\
721703 721686 724894 721064 723812 721097 730187 723726 727268 725293 721820 724680 725401 722007 724204 723805 725620 727938 723148 725288 725719 727934\
724183 727453 725208 726218 721907 724877 725430 724997 727347 727549 724163 724346 722271 724093 727058 725183 723947 722506 725519 723133 724367\
723260 725010 726929 724847 726959 723177 723363 724897 722266 724943 726652 721351 722140 724322 725511 726797 721815 727873 726559 724595 726515\
723411 722552 726523 722480 723252 721620 724441 725528 724788 724296 726201 725800 724860 721478 727128 724387 726977 725217 725698 726478 724199\
720893 725026 726131 721945 723996 725283 724576 726522 725939 726473 725817 725966 724533 723657 725430 726799 726950 725025 724348 723197 722097\
721515 724119 722445 724754 724575 722932 726172 724646 726487 724270 724966 726894 722776 724720 725374 724403 724265 723891 727018 725213 722447\
725564 726692 728678 726060 725131 721020 726564 722980 723576 725462 722896 722545 729202 725624 724871 724314 725534 724144 724655 722814 725574\
724985 724766 725034 723604 722843 724268 725581 724389 725379 727303 726027 724520 723844 726785 724384 722500 727173 725014 726861 722713 724898\
725633 725402 725197 724882 725968 726279 724051 724640 725070 725656 725849 724992 725398 726931 724011 726092 725189 724881 726380 725921 723508\
723801 722647 725571 725071 725615 723821 725878 724801 723297 723522 726741 725006 726868 723097 722454 725400 726336 726770 724213 726892 723735\
723965 723437 721171 724848 724442 726249 724052 721633 726365 723620 722816 723914 725057 725204 725070 724887 724684 724803 722529 728010 720530)\n"
pbs_string+=f"cat  {macrofile} \n "


###############################################################
###  Iterate through dimensions, materials, translations    ###
###        Create parameter list for Gate command           ###
###############################################################

if (gamma):
	particle_type_input="/gate/source/beam_g/setParticleType gamma"
	particle_outfilename="Gamma"
else:
	particle_type_input=" "
	particle_outfilename="Elec"


for blackout_first in ([True,False]):
	if blackout_first:
		for grating_thick in grating_thicknesses:
			if grating_thick>99:
				continue
			for BlackOut_thick in BlackOut_thickness:
				for peak_mat in peak_material:
					for blackout_mat in blackout_material:
							translation_BO_um=front_face_epi_um+(BlackOut_thick/2.0)
							translation_peak_um=front_face_epi_um+BlackOut_thick+(grating_thick/2.0)
							output_file_path=f"{out_dir}PhS3DoseFrom{particle_outfilename}_{grating_thick}umpeak_{BlackOut_thick}umBlackOut_peakMat_{peak_mat}_BOmat_{blackout_mat}_BlackOut-under-peaks"

							if not (os.path.isdir(output_file_path)):
								os.mkdir(output_file_path)

							translation_peak_mm=translation_peak_um/1000.0
							translation_BO_mm=translation_BO_um/1000.0

							param_list=f'[peakzlength_um,{grating_thick}] [peakztrans_mm,{translation_peak_mm}] [lightcoverzlength_um,{BlackOut_thick}]'
							param_list+=f' [lightcoverztrans_mm,{translation_BO_mm}] [pathOutputDose,{output_file_path}] [inputParticleType,{particle_type_input}] [pathGateMaterials,{materials_path}]'
							param_list+=f' [id,{file_number}] [inputPhaseSpaceFile,{phasespace_in}] [seed,{seed_rand}] [primaries,{how_many_primaries}]'
							param_list+=f' [lightcover_material,{blackout_mat}] [peak_material,{peak_mat}]]'


							mycommandpy=f"\"Gate {macrofile} -a '{param_list}'\"\n"
							# print (mycommand)
							pbs_string+=f"mycommand={mycommandpy}"
							pbs_string+=f"echo $mycommand \neval $mycommand\n"
							hadd_string+=f"hadd {output_file_path}/Total-Edep.root {output_file_path}/*Edep.root \n"
							hadd_string+=f"hadd {output_file_path}/Total-Edep-Squared.root {output_file_path}/*Edep-Squared.root \n"
							hadd_string+=f"hadd {output_file_path}/Total-NbOfHits.root {output_file_path}/*NbOfHits.root \n"
							pbs_string+="echo \"Time of interum job ending : $(date)\" \n"
							hadd_string+="echo \"Time of interum job ending : $(date)\" \n"


							print(param_list)
							print("")


	else:
		for grating_thick in grating_thicknesses:
			for BlackOut_thick in BlackOut_thickness:
				for peak_mat in peak_material:
					for blackout_mat in blackout_material:
						for distance_BlackOut_to_peaks_mm in BlackOut_distances:

							distance_BlackOut_to_peaks_um=distance_BlackOut_to_peaks_mm*1000 #mm
							translation_BO_um=front_face_epi_um+grating_thick+(BlackOut_thick/2.0)+distance_BlackOut_to_peaks_um
							translation_peak_um=front_face_epi_um+grating_thick/2.0
							output_file_path=f"{out_dir}PhS3DoseFromGamma_{grating_thick}umpeak_{BlackOut_thick}umBlackOut_peakMat_{peak_mat}_BOmat_{blackout_mat}_peaks-under-BlackOut_{distance_BlackOut_to_peaks_mm}mm"

							if not (os.path.isdir(output_file_path)):
								os.mkdir(output_file_path)

							translation_peak_mm=translation_peak_um/1000.0
							translation_BO_mm=translation_BO_um/1000.0

							param_list=f'[peakzlength_um,{grating_thick}] [peakztrans_mm,{translation_peak_mm}] [lightcoverzlength_um,{BlackOut_thick}]'
							param_list+=f' [lightcoverztrans_mm,{translation_BO_mm}] [pathOutputDose,{output_file_path}] [inputParticleType,/gate/source/beam_g/setParticleType gamma] [pathGateMaterials,{materials_path}]'
							param_list+=f' [id,{file_number}] [inputPhaseSpaceFile,{phasespace_in}] [seed,{seed_rand}] [primaries,{how_many_primaries}]'
							param_list+=f' [lightcover_material,{blackout_mat}] [peak_material,{peak_mat}]'


							mycommandpy=f"\"Gate {macrofile} -a '{param_list}'\"\n"
							# print (mycommand)
							pbs_string+=f"mycommand={mycommandpy}"
							pbs_string+=f"echo $mycommand \neval $mycommand\n"
							hadd_string+=f"hadd {output_file_path}/Total-Edep.root {output_file_path}/*Edep.root \n"
							hadd_string+=f"hadd {output_file_path}/Total-Edep-Squared.root {output_file_path}/*Edep-Squared.root \n"
							hadd_string+=f"hadd {output_file_path}/Total-NbOfHits.root {output_file_path}/*NbOfHits.root \n"
							pbs_string+="echo \"Time of interum job ending : $(date)\" \n"
							hadd_string+="echo \"Time of interum job ending : $(date)\" \n"

							print(param_list)
							print("")


pbs_string+="now=$(date) \necho \"Time of completion : $now\" " 
hadd_string+="now=$(date) \necho \"Time of completion : $now\" " 

print(pbs_string)

if gamma:
	script_ending="gamma"
else:
	script_ending="elec"

with open(f"flex_script_{script_ending}.pbs", "w") as text_file:
    print(pbs_string, file=text_file)

with open(f"hadd_flex_script_{script_ending}.pbs", "w") as text_file:
    print(hadd_string, file=text_file)
