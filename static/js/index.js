var info = {}
$(document).ready(function() {
    // 获取数据
    $('#user').blur(function() {
        var user = $('#user').val()
        if ( user.trim() === '') return;
        if (user) {
            getLearn(user)
        }
    })

    $('#submitCheckBox').click(function() {
        var user = $('#user').val();
        var pid = $('#pid').val();
        var checkedValues = [];
        if (pid.trim() === '' || user.trim() === '') {
            alert("请输入用户名和要学习的语言再提交");
            return;
        }

        $('#list-container input[type="checkbox"]:checked').each(function() {
            // Assuming the checkbox value holds the ID or relevant data
            checkedValues.push($(this).val());
        });
        const uniqueNumbers = new Set();
        checkedValues.forEach(item => {
            // 分割字符串
            const parts = item.split('_');
            // 遍历分割后的数组并将数字添加到 Set 中
            parts.forEach(part => {
                uniqueNumbers.add(parseInt(part, 10));
            });
        });

        // 将 Set 转换成数组
        const my_learn = Array.from(uniqueNumbers);

        const subject = getDescriptions(my_learn);
        if (my_learn.length===0) {
            alert("请选择内容再提交");
            return;
        }
        $.ajax({
            url: '/save_my_learn',
            type: 'POST',
            data: JSON.stringify({ 'user': user, 'pid': pid, 'my_learn': checkedValues, 'subject': subject }),
            contentType: 'application/json',
            success: function(response) {
                $('#user').attr('disabled',true)
                $('#language').attr('disabled',true)
                getLearn(user)
                console.log('Success:', response);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });

        function getDescriptions(numbers) {
            return numbers.reduce((acc, number) => {
                const description = info[number.toString()];
                if (description !== undefined) {
                    acc[number] = description;
                }
                return acc;
            }, {});
        }
    })

    // 用户选择或输入编程语言时触发
    $('#submitLanguage').click(function() {
        var language = $('#language').val();
        var user = $('#user').val();
        var readonly = 0
        if ($("#readonly").is(':checked')) {
            readonly = 1
        }
        if (language.trim() === '' || user.trim() === '') {
            alert("请输入用户名和要学习的语言");
            return;
        }
        // 发送 AJAX 请求到服务器
        $.ajax({
            url: '/learning',
            type: 'POST',
            data: { language: language, readonly: readonly },
            success: function(response) {
                // 清除之前的列表
                $('#list-container').empty();
                if (readonly === 1) {
                    $('#list-container').html(marked.parse(response))
                    return
                }
                // 初始化列表
                buildList(response, $('#list-container'), 0);
                // console.log(info)
                // 全选/取消全选逻辑
                $('input[type=checkbox]').on('change', function() {
                    var isChecked = $(this).prop('checked');
                    var subList = $(this).closest('div').find('input[type=checkbox]').not(this);
                    subList.prop('checked', isChecked);
                });
            },
            error: function() {
                alert("Failed to fetch the learning outline.");
            }
        });
    });
});

function getLearn(user) {
    $.ajax({
        url: '/learning', // 你要请求的URL
        type: 'GET', // 请求的类型是GET
        data: { user: user },
        dataType: 'json', // 预期服务器返回的数据类型，这里是JSON
        success: function(data) {
            $('#left').empty();
            buildLeft(data, $('#left'), 0);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // 请求失败时执行的回调函数
            console.error("请求失败: " + textStatus, errorThrown);
        }
    });
}

function learnSubject(pid, title) {
    var readonly = 0
    if ($("#readonly").is(':checked')) {
        readonly = 1
    }
    $.ajax({
        url: '/learn_subject', // 你要请求的URL
        type: 'GET', // 请求的类型是GET
        data: { pid: pid, subject: title, readonly: readonly },
        success: function(response) {
            // 清除之前的列表
            $('#list-container').empty();
            if (readonly === 1) {
                $('#list-container').html(marked.parse(response))
                return
            }
            // 初始化列表
            buildList(response, $('#list-container'), 0);
            // console.log(info)
            // 全选/取消全选逻辑
            $('input[type=checkbox]').on('change', function() {
                var isChecked = $(this).prop('checked');
                var subList = $(this).closest('div').find('input[type=checkbox]').not(this);
                subList.prop('checked', isChecked);
            });
        }
    });
}

function buildLeft(items, parent, hid) {
    items.forEach(function(it) {
        var $it = $('<div></div>');
        if (it.oid == 0) {
            hid = it.id
        }
        var $label = $('<a href="#" onClick="learnSubject('+it.id+',\''+it.title+'\')"></a>').text(it.title);
        $it.append($label);
        if (it.children && it.children.length > 0) {
            var $subList = $('<ul></ul>');
            $it.append($subList);
            buildLeft(it.children, $subList, hid);
        }
        parent.append($it);
    });
}

// 递归创建DOM节点
function buildList(items, parent, hid) {
    items.forEach(function(item) {
        info[item.id] = item.title
        var $item = $('<div></div>');

        if (item.order_id == 0) {
            hid = item.id
        }
        v = hid + '_' + item.order_id + '_' + item.bullet_id + '_' + item.id
        var $checkbox = $('<input type="checkbox" value="'+v+'">');
        var $label = $('<label></label>').text(item.title);
        $item.append($checkbox).append($label);
        if (item.children && item.children.length > 0) {
            var $subList = $('<ul></ul>');
            $item.append($subList);
            buildList(item.children, $subList, hid);
        }
        parent.append($item);
    });
}
