// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        // 日付をクリック、または範囲を選択したイベント
        selectable: true,
        select: function (info) {
            // alert("selected " + info.startStr + " to " + info.endStr);

            // 入力ダイアログ
            var eventName = prompt("イベントを入力してください");

            if (eventName) {

                // 登録処理の呼び出し
                axios
                    .post("/sc/add/", {
                        start_date: info.start.valueOf(),
                        end_date: info.end.valueOf(),
                        event_name: eventName,
                    })
                    .then(() => {
                        calendar.addEvent({
                            title: eventName,
                            start: info.start,
                            end: info.end,
                            allDay: true,
                        });
                        location.reload();
                    })
                    .catch(() => {
                        alert("登録に失敗しました");
                    });
            }
        },

        events: function (info, successCallback, failureCallback) {

            axios
                .post("/sc/list/", {
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    alert("一覧表示に失敗しました");
                });

        },

        eventClick: function(info) {
            var eventName = prompt("イベントを修正してください");

            console.log("🍭");

            if(eventName){
                axios
                    .post("/sc/edit/", {
                        id: info.event.id,
                        start_date: info.event.start.valueOf(),
                        end_date: info.event.end.valueOf(),
                        event_name: eventName,
                    })
                    .then(() => {
                        location.reload();
                    })
                    .catch(() => {
                        alert("更新に失敗しました");
                    });
            } else {
                axios
                    .delete("/sc/delete/" + info.event.id, {
                        id: info.event.id,
                    })
                    .then(() => {
                        location.reload();
                        alert("予定を削除しました");
                    })
                    .catch(() => {
                        alert("削除に失敗しました");
                    });
            }
        },
    });

    calendar.render();
});