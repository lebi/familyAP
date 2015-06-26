$(function () {
    var s = new WebSocket("ws://" + window.location.host + "/admin/videows");
    s.onopen = function () {
        console.log('WebSocket open');
        var createInfo={action:'new',target:'0.0.0.0'};
        sendInfo(createInfo);
    };

    s.onmessage = function(data){
        console.log(data.data)
        data=JSON.parse(data.data);
        console.log(data.action)
        switch ( data.action) {
            case 'answer' :
                offerer.setRemoteDescription(new RTCSessionDescription(data.answer))
                break
            case "ans_candidate":
                offerer.addIceCandidate(new RTCIceCandidate(data.candidate))
                break
            case "create":
                target=data.ip
                answererPeer(data.offer , data.stream)
                break
            case "off_candidate":
                answerer.addIceCandidate(new RTCIceCandidate(data.candidate))
                break
            case "new":
                userList=[]
                userList[0]=data;
                renderUserList(userList);
                break
            case "remove":
                // $('.live').append('<li onclick="chat(this)">'+data.username+'</li>');
                var ip=data.ip;
                $("#videoWrap .live li[ip='"+ip+"']").remove();
                break
        }
    }
    window.s = s;

    $.getJSON('videolist',function (data) {
        renderUserList(data.data);
    })


});


var mediaConstraints = {
    optional: [],
    mandatory: {
        OfferToReceiveAudio: false,
        OfferToReceiveVideo: true
    }
};

var offerer,answerer;
var local=document.getElementById('local');
var remote = document.getElementById('remote');

window.RTCPeerConnection = window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
window.RTCSessionDescription = window.mozRTCSessionDescription || window.RTCSessionDescription;
window.RTCIceCandidate = window.mozRTCIceCandidate || window.RTCIceCandidate;

navigator.getUserMedia = navigator.mozGetUserMedia || navigator.webkitGetUserMedia;
window.URL = window.webkitURL || window.URL;

window.iceServers = {iceServers: [{url: 'stun:23.21.150.121'}]};
/* offerer */
function offererPeer(video_stream) {
    offerer = new RTCPeerConnection(window.iceServers)
    offerer.addStream(video_stream)
    offerer.onaddstream = function (event) {

    }

    offerer.onicecandidate = function (event) {
        if (!event || !event.candidate) return;
        var json={'action' : 'off_candidate','candidate' :event.candidate,'target':target};
        sendInfo(json);
    }

    offerer.createOffer(function (offer) {
        offerer.setLocalDescription(offer)
        console.log(target);
        sendInfo({'action' : 'create','target':target,'offer':offer});
    }, function() {}, mediaConstraints)
}

function answererPeer(offer, video_stream) {
    answerer = new RTCPeerConnection(window.iceServers);

    answerer.onaddstream = function (event) {
        remote.src = URL.createObjectURL(event.stream);
        remote.play();
    };

    answerer.onicecandidate = function (event) {
        if (!event || !event.candidate) return;
        sendInfo({'action' : 'ans_candidate','candidate' :event.candidate,'target':target});
        //offerer.addIceCandidate(event.candidate);
    };

    answerer.setRemoteDescription(new RTCSessionDescription(offer));
    answerer.createAnswer(function (answer) {
        answerer.setLocalDescription(answer);
        sendInfo({'action' : 'answer' ,'answer' : answer, 'target':target});
    }, function() {}, mediaConstraints);
}
var video_constraints = {
    mandatory: {},
    optional: []
}

function getUserMedia(callback) {
    var n = navigator
    n.getMedia = n.webkitGetUserMedia || n.mozGetUserMedia
    n.getMedia({
        audio: false,
        video: video_constraints
    }, callback, onerror)

    function onerror(e) {
        alert(JSON.stringify(e, null, '\t'))
    }
}
function sendInfo(data){
    if(!window.s){
        alert("Please connect server.");
    }else{
        s.send(JSON.stringify(data));
    }
}

var target;
function renderUserList(userList){
    var temp=_.template($("#video-template").html());
    $("#videoWrap .live").append(temp({userList:userList}));

    $('#videoWrap .live li').click(function(){
        target=$(this).attr('ip');
        getUserMedia(function (video_stream) {
            offererPeer(video_stream,target)
            local.src = window.URL.createObjectURL(video_stream);
            local.play();
        });
    })
}